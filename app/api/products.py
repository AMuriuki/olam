from app.api import bp
from flask import request, jsonify
from app.api.auth import token_auth
from app.main.models.product import Product


@bp.route('/get_product/<id>', methods=['GET'])
# @token_auth.login_required
def get_product(id):
    return jsonify(Product.query.get_or_404(id).to_dict())
