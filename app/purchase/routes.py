from datetime import datetime
from itertools import product
from pstats import Stats
from flask import jsonify, render_template, request, session
from flask_login import current_user, login_required
from app import purchase
from app.decorators import active_user_required, can_create_access_required, module_access_required
from flask_babel import _, get_locale
from app.main.models.product import Product
from app.purchase import bp
from app.purchase.models.product import ProductPurchase
from app.purchase.models.purchase import Purchase, PurchaseStatus
from app.purchase.forms import PurchaseForm
from app import db


@bp.route('/', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(4)
def index():
    purchases = Purchase.query.all()
    return render_template("purchase/index.html", title=_("Purchase Orders | Olam ERP"), purchases=purchases)


@bp.route('/new/request-for-quotation', methods=['GET', 'POST'])
@login_required
@active_user_required
@can_create_access_required(4)
def new_request_for_quotation():
    new = True
    form = PurchaseForm()
    statuses = PurchaseStatus.query.all()
    products = Product.query.all()
    if request.method == "POST":
        if 'vendor' in request.form:
            vendor = request.form['vendor']
        else:
            vendor = None
        if 'due_date' in request.form:
            due_date = request.form['due_date']
        else:
            due_date = None
        if 'purchase_id' in request.form:
            purchase_id = request.form['purchase_id']
        else:
            purchase_id = None
        if 'time' in request.form:
            time = request.form['time']
        else:
            time = None
        if 'product_id' in request.form:
            product_id = request.form['product_id']
        else:
            product_id = None
        if 'quantity' in request.form:
            quantity = request.form['quantity']
        else:
            quantity = None
        if purchase_id and Purchase.query.filter_by(id=purchase_id).first():
            purchase = Purchase.query.filter_by(id=purchase_id).first()
            if vendor:
                purchase.vendor = vendor
                purchase.updated_on = datetime.utcnow()
                db.session.commit()
            if due_date:
                purchase.due_date = due_date
                purchase.updated_on = datetime.utcnow()
                db.session.commit()
            if time:
                purchase.time = time
                purchase.updated_on = datetime.utcnow()
                db.session.commit()
            if quantity:
                purchase_product = ProductPurchase.query.filter_by(
                    purchase_id=purchase_id).first()
                purchase_product.quantity = quantity
                db.session.commit()
            if product_id:
                purchase_product = ProductPurchase(
                    product_id=product_id, purchase_order_id=purchase_id, vendor_id=purchase.vendor)
                db.session.add(purchase_product)
                db.session.commit()
        else:
            purchase = Purchase(
                vendor=vendor, representative=current_user.get_id())
            purchase.generate_reference()
            db.session.add(purchase)
            db.session.commit()
        return jsonify({"success": True, "purchase_id": purchase.id})
    return render_template("purchase/purchase_order.html", title=_("New Request for Quotation | Olam ERP"), statuses=statuses, new=new, form=form, products=products)
