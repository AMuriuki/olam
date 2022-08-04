from math import prod
import os
from unicodedata import category
from flask import jsonify, make_response, render_template, request, session
from flask_login import current_user, login_required
from itsdangerous import json
import requests
from app.decorators import active_user_required, can_create_access_required, model_access_required, module_access_required
from app.inventory import bp
from app.inventory.forms import NewProductForm
from app.inventory.utils import product_model
from app.main.models.company import Company
from app.main.models.product import FILTERS, Product, ProductAttribute, ProductAttributeValue, ProductCategory, ProductImage, ProductType
from flask_babel import _
from app import db, tenant_site
from app.utils import remove_comma
from threading import Thread
from app.database import insert_product


@bp.route('/index', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(5)
def index():
    return render_template("inventory/index.html", title=_("Inventory | Olam ERP"))


@bp.route('/products', methods=['GET', 'POST'])
@login_required
@model_access_required(9)
@active_user_required
def products():
    filters = FILTERS
    selected_filters = 'Products'
    products = Product.query.all()
    return render_template("inventory/products.html", title=_("Products | Olam ERP"), products=products, filters=filters, selectedFilters=selected_filters)


@bp.route('/new/product', methods=['GET', 'POST'])
@login_required
@can_create_access_required(9)
@active_user_required
def create_product():
    company = Company.query.first()
    attributes = ProductAttribute.query.all()

    if request.method == "POST":

        if request.form['price']:
            price = float(remove_comma(request.form['price']))
            total_price = (price * float(company.tax))/100 + price

        if 'promo' in request.form:
            promo = True
        else:
            promo = False

        if 'category_id' in request.form:
            if request.form['category_id']:
                category_id = request.form['category_id']
            else:
                category_id = None
        else:
            category_id = None

        if 'uom_id' in request.form:
            if request.form['uom_id']:
                uom_id = request.form['uom_id']
            else:
                uom_id = None
        else:
            uom_id = None

        if 'preview_mode' in request.form:
            if request.form['preview_mode']:
                status = True
            else:
                status = False
        else:
            status = False

        product = Product.query.filter_by(name=request.form['name']).first()
        if product:
            parent_id = product.id
        else:
            parent_id = None
        
        product = Product(name=request.form['name'] if request.form['name'] else None, type_id=request.form['product_type'] if request.form['product_type'] else None, category_id=category_id, price=remove_comma(request.form['price']) if request.form['price'] else None, total_price=total_price, cost=remove_comma(request.form['cost']) if request.form['cost'] else None, uom_id=uom_id, quantity=request.form['quantity'] if request.form['quantity'] else None, tax=request.form['tax'] if request.form['tax'] else None, created_by=current_user.id, promo=promo, promo_start=request.form['promo_start'] if request.form['promo_start'] else None, promo_end=request.form['promo_end'] if request.form['promo_end'] else None, promo_price=request.form['promo_price'] if request.form['promo_price'] else None, draft=status, parent_id=parent_id, description = request.form['description'] if request.form['description'] else None)
        product.generate_sku()
        db.session.add(product)
        db.session.commit()

        selected_attributes = []
        for attribute in attributes:
            if request.form['hidden-inp-'+str(attribute.id)]:
                product_attribute_value = ProductAttributeValue(
                    product_id=product.id, attribute_id=attribute.id, attribute_value_id=request.form['hidden-inp-'+str(attribute.id)])
                db.session.add(product_attribute_value)
                db.session.commit()
                selected_attributes.append(product_attribute_value.to_dict())

        product_dict = {
            'name': product.name,
            'category': product.category.name,
            'price': product.total_price,
            'quantity': product.quantity,
            'promo': product.promo,
            'promo_start': product.promo_start,
            'promo_end': product.promo_end,
            'promo_price': product.promo_price,
            'id': str(product.id),
            'sku': product.sku,
            'attributes': [selected_attributes]
        }

        print(product_dict)

        post_response = requests.post(
            tenant_site+'/api/product/', json=product_dict)
        if post_response.status_code == 200:
            pass

        files = request.files.getlist('files')
        if files:
            paths = []
            for file in files:
                filename = file.filename
                file.save(filename)
                paths.append(os.path.abspath(filename))
            current_user.launch_task(
                'upload_product_images', 'upload images', 'background_task', paths, product.id)

        return jsonify({'success': True, 'product_id': product.id})

    form = NewProductForm()
    categories = ProductCategory.query.all()
    types = ProductType.query.all()
    return render_template("inventory/new_product.html", title=_("New Product | Olam ERP"), form=form, categories=categories, types=types, attributes=attributes)


@ bp.route('/product/<product_id>', methods=['GET', 'POST'])
@ login_required
@ model_access_required(9)
@ active_user_required
def product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    products = Product.query.all()
    attributes = ProductAttributeValue.query.filter_by(
        product_id=product.id).all()
    images = ProductImage.query.filter_by(product_id=product.id).all()
    for idx, p in enumerate(products):
        if str(p.id) == product_id:
            current_index = idx
            prev_index = current_index - 1
            next_index = current_index + 1
    return render_template("inventory/product.html", title=_("Product | Olam ERP"), product=product, prev_index=prev_index, next_index=next_index, products=products, current_index=current_index+1, attributes=attributes, images=images)


@ bp.route('/product/edit/<product_id>', methods=['GET', 'POST'])
@ login_required
@ model_access_required(9)
@ active_user_required
def edit_product(product_id):
    company = Company.query.first()
    product = Product.query.filter_by(id=product_id).first()
    attributes = ProductAttributeValue.query.filter_by(
        product_id=product.id).all()

    if request.method == "POST":

        if request.form['price']:
            price = float(remove_comma(request.form['price']))
            total_price = (price * float(company.tax))/100 + price

        if 'promo' in request.form:
            promo = True
        else:
            promo = False

        if 'category_id' in request.form:
            if request.form['category_id']:
                category_id = request.form['category_id']
            else:
                category_id = None
        else:
            category_id = None

        if 'uom_id' in request.form:
            if request.form['uom_id']:
                uom_id = request.form['uom_id']
            else:
                uom_id = None
        else:
            uom_id = None

        if 'preview_mode' in request.form:
            if request.form['preview_mode']:
                status = True
            else:
                status = False
        else:
            status = False

        product = Product.query.filter_by(name=request.form['name']).first()
        if product:
            parent_id = product.id
        else:
            parent_id = None
        
        product.name = request.form['name'] if request.form['name'] else None
        product.type_id = request.form['product_type'] if request.form['product_type'] else None
        product.category_id = category_id
        product.price = remove_comma(
            request.form['price']) if request.form['price'] else None
        product.total_price = total_price
        product.cost = remove_comma(
            request.form['cost']) if request.form['cost'] else None
        product.uom_id = uom_id
        product.quantity = request.form['quantity'] if request.form['quantity'] else None
        product.tax = request.form['tax'] if request.form['tax'] else None
        product.description = request.form['description'] if request.form['description'] else None
        product.promo = promo
        product.promo_start = request.form['promo_start'] if request.form['promo_start'] else None
        product.promo_end = request.form['promo_end'] if request.form['promo_end'] else None
        product.promo_price = request.form['promo_price'] if request.form['promo_price'] else None
        product.draft = status
        product.parent_id = parent_id
        db.session.commit()

        for attribute in attributes:
            if request.form['hidden-inp-'+str(attribute.attribute.id)]:
                product_attribute_value = ProductAttributeValue.query.filter_by(
                    product_id=product.id, attribute_id=attribute.attribute.id).first()
                if product_attribute_value:
                    product_attribute_value.attribute_value_id = request.form['hidden-inp-'+str(
                        attribute.attribute.id)]
                    db.session.commit()

        files = request.files.getlist('files')
        if files:
            paths = []
            for file in files:
                filename = file.filename
                file.save(filename)
                paths.append(os.path.abspath(filename))
            current_user.launch_task(
                'upload_product_images', 'upload images', paths, product.id)

        return jsonify({'success': True, 'product_id': product.id})
    form = NewProductForm()
    categories = ProductCategory.query.all()
    types = ProductType.query.all()
    return render_template("inventory/edit_product.html", title=_("Edit Product | Olam ERP"), form=form, product=product, categories=categories, types=types, attributes=attributes)
