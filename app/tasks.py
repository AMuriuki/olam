from concurrent.futures import process
from locale import currency
from math import prod
from threading import Thread
from app.auth.models.user import Access, Group, Users
from app.auth.routes import get_access_groups
from app.auth.utils import get_users
from app.contacts.utils import get_partner_tags, get_partner_titles, get_partners
from app.crm.models.crm_recurring_plan import RecurringPlan
from app.crm.models.crm_stage import Stage
from app.crm.models.crm_lead import Lead
from app.helper_functions import set_default_user_groups
from app.main.models.activities import Activity, ActivityType
from app.main.models.company import Company
from app.main.models.module import Model, Module, ModuleCategory
from app.main.models.partner import Partner, PartnerTag, PartnerTitle
from app.main.models.country import City, Country
from flask import current_app
from app import db
from app.main.models.product import Product, ProductAttribute, ProductAttributeValue, ProductCategory, ProductType
from app.main.models.uom import Uom, UomCategory
from app.models import Task
from app.main.utils import get_activities, get_activity_types, get_calling_codes, get_company, get_countries, get_countries_cities, get_models, get_moduleCategories, get_modules, get_product_attribute_values, get_product_attributes, get_product_categories, get_product_models, get_product_types, get_products, get_uom_categories, get_uoms
from app.crm.utils import get_opportunities, get_recurring_plans, get_stages
from rq import get_current_job
from app.models import Task
from app import create_app, db
from werkzeug.security import generate_password_hash
from app.purchase.models.purchase import Purchase, PurchaseActivity, PurchaseStatus
from app.purchase.utils import get_purchase_status, get_purchases
import traceback
from app.settings.utils import get_accessGroups, get_accessGroupsRights, get_accessRights


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

        # company details
        companies = get_company()
        for company in companies:
            exists = Company.query.filter_by(name=company['name']).first()
            if not exists:
                record = Company(
                    name=company['name'], domain_name=company['domain_name'], currency=company['currency'])
                db.session.add(record)
                db.session.commit()

        # partners
        partners = get_partners()
        for partner in partners:
            exists = Partner.query.filter_by(id=partner['id']).first()
            if not exists:
                if 'is_company' in partner:
                    if partner['is_company'] == True:
                        record = Partner(id=partner['id'], company_name=partner['company_name'], email=partner['email'], is_company=partner['is_company'], is_active=partner['is_active'], phone_no=partner['phone_no'],
                                         website=partner['website'], postal_code=partner['postal_code'], postal_address=partner['postal_address'])
                        record.generate_slug()
                        db.session.add(record)
                        db.session.commit()
                if 'is_tenant' in partner:
                    if partner['is_tenant'] == True:
                        record = Partner(id=partner['id'], name=partner['name'], email=partner['email'], phone_no=partner['phone_no'],
                                         is_active=partner['is_active'], company_id=partner['company_id'], is_tenant=partner['is_tenant'])
                        record.generate_slug()
                        db.session.add(record)
                        db.session.commit()
                if 'parent_id' in partner:
                    record = Partner(id=partner['id'], name=partner['name'], title=partner['title'], function=partner['function'], email=partner['email'], phone_no=partner['phone_no'],
                                     is_active=partner['is_active'], parent_id=partner['parent_id'], is_individual=partner['is_individual'], website=partner['website'])
                    record.generate_slug()
                    db.session.add(record)
                    db.session.commit()
                print("Partner " + record.get_name() + " added")

        # partner tags
        partner_tags = get_partner_tags()
        for tag in partner_tags:
            exists = PartnerTag.query.filter_by(id=tag['id']).first()
            if not exists:
                record = PartnerTag(id=tag['id'], name=tag['name'])
                db.session.add(record)
                db.session.commit()
                print("Partner Tag " + record.name + " added")

        # partner titles
        partner_titles = get_partner_titles()
        for title in partner_titles:
            exists = PartnerTitle.query.filter_by(id=title['id']).first()
            if not exists:
                record = PartnerTitle(id=title['id'], name=title['name'])
                db.session.add(record)
                db.session.commit()
                print("Partner title " + record.name + " added")

        # users
        users = get_users()
        for user in users:
            exists = Users.query.filter_by(id=user['id']).first()
            if not exists:
                record = Users(id=user['id'], partner_id=user['partner_id'],
                               company_id=user['company_id'], is_active=user['is_active'])
                record.generate_slug()
                record.password_hash = generate_password_hash(user['password'])
                db.session.add(record)
                db.session.commit()

        # module categories
        module_categories = get_moduleCategories()
        for module_category in module_categories:
            exists = ModuleCategory.query.filter_by(
                id=module_category['category_id']).first()
            if not exists:
                moduleCategory = ModuleCategory(
                    id=module_category['category_id'], name=module_category['category_name'])
                db.session.add(moduleCategory)
                db.session.commit()

        # installed modules
        modules = get_modules()
        for module in modules:
            exists = Module.query.filter_by(id=module['id']).first()
            if not exists:
                record = Module(id=module['id'], technical_name=module['technical_name'], official_name=module['official_name'], bp_name=module['bp_name'],
                                summary=module['summary'], category_id=module['category_id'], user_groups_api=module['user_groups_api'], models_api=module['models_api'], url=module['url'])
                db.session.add(record)
                db.session.commit()

        # access groups
        access_groups = get_accessGroups()
        for access_group in access_groups:
            exists = Group.query.filter_by(id=access_group['id']).first()
            if not exists:
                record = Group(id=access_group['id'], name=access_group['name'], module_id=access_group['module_id'],
                               permission=access_group['permission'], access_rights_url=access_group['access_rights_url'])
                record.generate_slug()
                db.session.add(record)
                db.session.commit()

        user = Users.query.filter_by(id=1).first()
        groups = Group.query.filter_by(permission=3).all()
        for group in groups:
            group.users.append(user)
            db.session.commit()

        users = Users.query.filter(Users.id != 1).all()
        for user in users:
            set_default_user_groups(user)

        # models
        models = get_models()
        for model in models:
            exists = Model.query.filter_by(id=model['id']).first()
            if not exists:
                record = Model(id=model['id'], name=model['name'],
                               description=model['description'])
                record.generate_slug()
                db.session.add(record)
                db.session.commit()
                print("Model: " + model['name'] + " added")

        # access rights
        access_rights = get_accessRights()
        assosciations = get_accessGroupsRights()
        for access_right in access_rights:
            exists = Access.query.filter_by(id=access_right['id']).first()
            if not exists:
                access = Access(id=access_right['id'], name=access_right['name'], model_id=access_right['model_id'],
                                read=access_right['read'], write=access_right['write'], create=access_right['create'], delete=access_right['delete'])
                db.session.add(access)
                db.session.commit()
                item = next(
                    item for item in assosciations if item['access_id'] == access.id)
                group = Group.query.filter_by(
                    id=item['group_id']).first()
                group.rights.append(access)
                db.session.commit()
                print("Access: " + access.name + " added")

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
                print("Opportunity: " + lead.name + " added")

        # activity types
        activity_types = get_activity_types()
        for activity_type in activity_types:
            exists = ActivityType.query.filter_by(
                id=activity_type['id']).first()
            if not exists:
                activitytype = ActivityType(
                    id=activity_type['id'], name=activity_type['name'], model_id=activity_type['model_id'])
                db.session.add(activitytype)
                db.session.commit()
                print("Activity type " + str(activitytype.id) + " created")

        # purchase statuses
        purchase_statuses = get_purchase_status()
        for purchase_status in purchase_statuses:
            exists = PurchaseStatus.query.filter_by(
                id=purchase_status['id']).first()
            if not exists:
                purchasestatus = PurchaseStatus(
                    id=purchase_status['id'], name=purchase_status['name'])
                db.session.add(purchasestatus)
                db.session.commit()
                print("Purchase status " +
                      purchase_status['name'] + " created")

        # uom categories
        uom_categories = get_uom_categories()
        for uom_category in uom_categories:
            exists = UomCategory.query.filter_by(id=uom_category['id']).first()
            if not exists:
                category = UomCategory(
                    id=uom_category['id'], name=uom_category['name'])
                db.session.add(category)
                db.session.commit()
                print("UOM Category " + str(category.name) + " created")

        # uoms
        uoms = get_uoms()
        for uom in uoms:
            exists = Uom.query.filter_by(id=uom['id']).first()
            if not exists:
                u_o_m = Uom(id=uom['id'], name=uom['name'],
                            category_id=uom['category_id'])
                db.session.add(u_o_m)
                db.session.commit()
                print("UOM " + str(u_o_m.name) + " created")

        # purchase records
        purchases = get_purchases()
        for purchase in purchases:
            exists = Purchase.query.filter_by(id=purchase['id']).first()
            if not exists:
                _purchase = Purchase(id=purchase['id'], reference=purchase['reference'], vendor=purchase['vendor'],
                                     representative=purchase['representative'], total=purchase['total'], status=purchase['status'])
                db.session.add(_purchase)
                db.session.commit()
                print("Purchase record " + purchase['vendor'] + " created")

        # product types
        product_types = get_product_types()
        for product_type in product_types:
            exists = ProductType.query.filter_by(id=product_type['id']).first()
            if not exists:
                producttype = ProductType(
                    id=product_type['id'], name=product_type['name'])
                db.session.add(producttype)
                db.session.commit()
                print("Product type " + str(producttype.name) + " created")

        # product attributes
        attributes = get_product_attributes()
        for attribute in attributes:
            exists = ProductAttribute.query.filter_by(
                id=attribute['id']).first()
            if not exists:
                product_attribute = ProductAttribute(
                    id=attribute['id'], name=attribute['name'])
                db.session.add(product_attribute)
                db.session.commit()
                print("Product attribute " +
                      str(product_attribute.name) + " created")

        # product attribute values
        attribute_values = get_product_attribute_values()
        for attribute_value in attribute_values:
            exists = ProductAttributeValue.query.filter_by(
                id=attribute_value['id']).first()
            if not exists:
                product_attribute_value = ProductAttributeValue(
                    id=attribute_value['id'], name=attribute_value['name'], attribute_id=attribute_value['attribute_id'])
                db.session.add(product_attribute_value)
                db.session.commit()
                print("Product attribute value " +
                      str(product_attribute_value.name) + " created")

        # product categories
        categories = get_product_categories()
        for category in categories:
            exists = ProductCategory.query.filter_by(
                id=category['id']).first()
            if not exists:
                product_category = ProductCategory(
                    id=category['id'], name=category['name'])
                db.session.add(product_category)
                db.session.commit()
                print("Product category " + category['name'] + " created")

        # products
        products = get_products()
        for product in products:
            exists = Product.query.filter_by(id=product['id']).first()
            if not exists:
                product_record = Product(id=product['id'], name=product['name'], manufacturer_id=product['manufacturer_id'], model_id=product['model_id'], category_id=product['category_id'],
                                         cost=product['cost'], price=product['price'], sku=product['sku'], processor_id=product['processor_id'], memory_id=product['memory_id'], storage_id=product['storage_id'])
                product_record.generate_sku()
                db.session.add(product_record)
                db.session.commit()
                print("Product record " + product_record.name + " created")

    except Exception as e:
        print(e)
        print(traceback.format_exc())
