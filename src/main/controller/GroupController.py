from flask import request, Response, jsonify, Blueprint
from src.main.db.models import Group
from src.main.extensions import db, jwt
from src.main.utils.password_validator import is_valid_length, is_on_blacklist, contains_pii
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    get_jwt_identity, set_access_cookies, set_refresh_cookies, 
    unset_jwt_cookies, 
)

group_bp = Blueprint("group_bp", __name__, url_prefix="/api/groups")



@group_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_groups():
    groups = Group.query.all()
    groups_list = [group.to_dict() for group in groups]
    return jsonify(groups_list), 200