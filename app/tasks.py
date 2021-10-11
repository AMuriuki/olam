from app.crm.models.crm_recurring_plan import RecurringPlan
from app.crm.models.crm_stage import Stage
from app.main.models.country import City, Country
from flask import current_app
from app import db
from app.models import Task
from app.main.utils import get_calling_codes, get_countries, get_countries_cities
from app.crm.utils import get_recurring_plans, get_stages
from rq import get_current_job
from app.models import Task
from app import create_app, db
import time

app = create_app()
app.app_context().push()


class ManageTasks(object):

    def _set_task_progress(progress):
        job = get_current_job()
        if job:
            job.meta['progress'] = progress
            job.save_meta()
            task = Task.query.get(job.get_id())
            task.user.add_notification(
                'task_progress', {'task_id': job.get_id(), 'progress': progress})

            if progress >= 100:
                task.complete = True
            db.session.commit()

    def _update_job_progress():
        job = get_current_job()
        print(job.get_id())
        if job:
            task = Task.query.get(job.get_id())
            task.complete = True
            db.session.commit()

    def launch_task(name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name)
        task = Task(id=rq_job.get_id(), name=name,
                    description=description)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return True if Task.query.filter_by(name=name, user=self, complete=False).first() else False


def seed_database():
    try:
        # Stages
        stages = get_stages()
        for stage in stages:
            exists = Stage.query.filter_by(name=stage['name']).first()
            if exists:
                pass
            else:
                stage = Stage(id=stage['id'], name=stage['name'])
                db.session.add(stage)
                db.session.commit()

        # Recurring Plans
        plans = get_recurring_plans()
        for plan in plans:
            exists = RecurringPlan.query.filter_by(name=plan['name']).first()
            if exists:
                pass
            else:
                recurring_plan = RecurringPlan(
                    id=plan['id'], name=plan['name'])
                db.session.add(recurring_plan)
                db.session.commit()

        # Countries
        countries = get_countries()
        for country in countries:
            exists = Country.query.filter_by(name=country['Name']).first()
            if exists:
                pass
            else:
                country = Country(name=country['Name'], code=country['Code'])
                db.session.add(country)
                db.session.commit()

        # Calling Code
        calling_codes = get_calling_codes()
        for calling_code in calling_codes:

            exists = Country.query.filter(((Country.calling_code == calling_code['Dial']) & (
                Country.name == calling_code['Country_Name'])) | ((Country.calling_code == calling_code['Dial']) & (
                    Country.code == calling_code['ISO3166_1_Alpha_2']))).first()
            if exists:
                pass
            else:
                country = Country.query.filter((
                    Country.name == calling_code['Country_Name']) | (
                    Country.code == calling_code['ISO3166_1_Alpha_2'])).first()
                if country:
                    country.calling_code = calling_code['Dial']
                    country.currency_name = calling_code['ISO4217_Currency_Name']
                    country.currency_alphabetic_code = calling_code['ISO4217_Currency_Alphabetic_Code']
                    country.currency_numeric_code = calling_code['ISO4217_Currency_Numeric_Code']
                    country.languages = calling_code['Languages']
                    db.session.commit()

        # Cities
        cities = get_countries_cities()
        for city in cities:
            print(city)
            country = Country.query.filter_by(name=city['country']).first()
            if not country:
                country = Country(name=city['country'])
                db.session.add(country)
                db.session.commit()
            exists = City.query.filter_by(geonameid=city['geonameid']).first()
            if exists:
                pass
            else:
                city = City(
                    name=city['name'], country_id=country.id, geonameid=city['geonameid'])
                db.session.add(city)
                db.session.commit()
    except Exception as e:
        print(e)
    finally:
        ManageTasks._update_job_progress()
