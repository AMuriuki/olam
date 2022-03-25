from flask import request, jsonify
from app.api import bp
from app.main.models.module import Model, Module, ModuleCategory
from app.api.auth import token_auth
from flask_login import current_user


@bp.route('/get_modules', methods=['GET'])
@token_auth.login_required
def get_modules():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Module._to_collection_dict(
        Module.query, page, per_page, 'api.get_modules')
    return jsonify(data)
