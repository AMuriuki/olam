from flask import render_template
from flask_login import login_required
from app.decorators import active_user_required, module_access_required
from flask_babel import _, get_locale
from app.purchase import bp


@bp.route('/', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(4)
def index():
    purchases = ""
    return render_template("purchase/index.html", title=_("Purchase Orders | Olam ERP"), purchases=purchases)
