from app import db
from app.settings import bp
from flask_login import login_required


@bp.route('/')
@login_required
def index():
    pass
