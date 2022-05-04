from flask import jsonify, render_template, request, session
from flask_login import current_user, login_required
from app.decorators import active_user_required, can_create_access_required, model_access_required, module_access_required
from app.inventory import bp
from app.inventory.forms import NewProductForm
from app.main.models.product import FILTERS, Product, ProductCategory, ProductType
from flask_babel import _
from app import db


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
    if request.form:
        product = Product(name=request.form['name'] if request.form['name'] else None, type_id=request.form['product_type'] if request.form['product_type'] else None, category_id=request.form['category'] if request.form['category'] else None, price=request.form['price'] if request.form['price']
                          else None, cost=request.form['cost'] if request.form['cost'] else None, uom_id=request.form['uom'] if request.form['uom'] else None, quantity=request.form['quantity'] if request.form['quantity'] else None, tax=request.form['tax'] if request.form['tax'] else None, created_by=current_user.id)
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
