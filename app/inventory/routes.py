from unicodedata import category
from flask import jsonify, make_response, render_template, request, session
from flask_login import current_user, login_required
from app.decorators import active_user_required, can_create_access_required, model_access_required, module_access_required
from app.inventory import bp
from app.inventory.forms import NewProductForm
from app.main.models.company import Company
from app.main.models.product import FILTERS, Product, ProductCategory, ProductType
from flask_babel import _
from app import db
from app.utils import remove_comma


@bp.route('/index', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(5)
def index():
    return render_template("inventory/index.html", title=_("Inventory | Olam ERP"))


@bp.route('/products', methods=['GET', 'POST'])
@model_access_required(9)
@active_user_required
def products():
    filters = FILTERS
    selected_filters = 'Products'
    products = Product.query.all()
    return render_template("inventory/products.html", title=_("Products | Olam ERP"), products=products, filters=filters, selectedFilters=selected_filters)


@bp.route('/new/product', methods=['GET', 'POST'])
@can_create_access_required(9)
@active_user_required
def create_product():
    company = Company.query.first()
    if request.form:
        if request.form['price']:
            price = float(remove_comma(request.form['price']))
            total_price = (price * float(company.tax))/100 + price

        product = Product(name=request.form['name'] if request.form['name'] else None, type_id=request.form['product_type'] if request.form['product_type'] else None, category_id=request.form['category_id'] if 'category_id' in request.form else None, price=remove_comma(request.form['price']) if request.form['price'] else None,
                          total_price=total_price, cost=remove_comma(request.form['cost']) if request.form['cost'] else None, uom_id=request.form['uom_id'] if request.form['uom_id'] else None, quantity=request.form['quantity'] if request.form['quantity'] else None, tax=request.form['tax'] if request.form['tax'] else None, created_by=current_user.id)
        db.session.add(product)
        db.session.commit()
        return jsonify({'success': True, 'product_id': product.id})

    form = NewProductForm()
    categories = ProductCategory.query.all()
    types = ProductType.query.all()
    return render_template("inventory/new_product.html", title=_("New Product | Olam ERP"), form=form, categories=categories, types=types)


@bp.route('/product/<product_id>', methods=['GET', 'POST'])
@model_access_required(9)
@active_user_required
def product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    products = Product.query.all()

    for idx, p in enumerate(products):
        if str(p.id) == product_id:
            current_index = idx
            prev_index = current_index - 1
            next_index = current_index + 1
    return render_template("inventory/product.html", title=_("Product | Olam ERP"), product=product, prev_index=prev_index, next_index=next_index, products=products, current_index=current_index+1)


@bp.route('/product/edit/<product_id>', methods=['GET', 'POST'])
@model_access_required(9)
@active_user_required
def edit_product(product_id):
    company = Company.query.first()
    product = Product.query.filter_by(id=product_id).first()
    if request.form:
        if request.form['price']:
            price = float(remove_comma(request.form['price']))
            total_price = (price * float(company.tax))/100 + price

        product.name = request.form['name'] if request.form['name'] else None
        product.type_id = request.form['product_type'] if request.form['product_type'] else None
        product.category_id = request.form['category_id'] if 'category_id' in request.form else None
        product.price = remove_comma(
            request.form['price']) if request.form['price'] else None
        product.total_price = total_price
        product.cost = remove_comma(
            request.form['cost']) if request.form['cost'] else None
        product.uom_id = request.form['uom_id'] if request.form['uom_id'] else None
        product.quantity = request.form['quantity'] if request.form['quantity'] else None
        product.tax = request.form['tax'] if request.form['tax'] else None
        db.session.commit()
        return jsonify({'success': True, 'product_id': product.id})
    form = NewProductForm()
    categories = ProductCategory.query.all()
    types = ProductType.query.all()
    return render_template("inventory/edit_product.html", title=_("Edit Product | Olam ERP"), form=form, product=product, categories=categories, types=types)
