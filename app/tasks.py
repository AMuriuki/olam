from app.contacts.utils import get_partners
from app.crm.models.crm_recurring_plan import RecurringPlan
from app.crm.models.crm_stage import Stage
from app.crm.models.crm_lead import Lead
from app.main.models.partner import Partner
from app.main.models.country import City, Country
from flask import current_app
from app import db
from app.models import Model, Task
from app.main.utils import get_calling_codes, get_countries, get_countries_cities, get_models
from app.crm.utils import get_opportunities, get_recurring_plans, get_stages
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
                stage = Stage(
                    id=stage['id'], name=stage['name'], position=stage['position'])
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


def dummy_data():
    try:
        # partners
        partners = get_partners()
        for partner in partners:
            exists = Partner.query.filter_by(id=partner['id']).first()
            if exists:
                pass
            else:
                if partner['is_company'] == True:
                    partner = Partner(id=partner['id'], company_name=partner['company_name'], email=partner['email'], is_company=partner['is_company'], is_active=partner['is_active'], phone_no=partner['phone_no'],
                                      website=partner['website'], postal_code=partner['postal_code'], postal_address=partner['postal_address'], city_id=partner['city_id'], country_id=partner['country_id'])
                    partner.generate_slug()
                    db.session.add(partner)
                    db.session.commit()

        # opportunities
        opportunities = get_opportunities()
        for opportunity in opportunities:
            exists = Lead.query.filter_by(id=opportunity['id']).first()
            if exists:
                pass
            else:
                lead = Lead(id=opportunity['id'], name=opportunity['name'], user_id=opportunity['user_id'], partner_id=opportunity['partner_id'], priority=opportunity['priority'], stage_id=opportunity['stage_id'], partner_email=opportunity['partner_email'],
                            partner_phone=opportunity['partner_phone'], plan_id=opportunity['plan_id'], partner_currency=opportunity['partner_currency'], active=opportunity['active'], expected_revenue=opportunity['expected_revenue'])
                lead.generate_slug()
                db.session.add(lead)
                db.session.commit()

        # models
        models = get_models()
        for model in models:
            exists = Model.query.filter_by(id=model['id']).first()
            if exists:
                pass
            else:
                model = Model(id=model['id'], name=model['name'],
                              description=model['description'])
                model.generate_slug()
                db.session.add(model)
                db.session.commit()

    except Exception as e:
        print(e)
