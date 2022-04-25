from flask import jsonify, render_template, request, session
from flask_login import login_required
from app.decorators import active_user_required, can_create_access_required, model_access_required, module_access_required
from app.inventory import bp
from app.inventory.forms import NewProductForm
from app.main.models.product import FILTERS, Product
from flask_babel import _


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
    form = NewProductForm()
    return render_template("inventory/new_product.html", title=_("New Product | Olam ERP"), form=form)
