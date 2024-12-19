from flask import request, Response, jsonify, Blueprint
from src.main.db.models import User
from src.main.extensions import db, jwt
from src.main.utils.password_validator import is_valid_length, is_on_blacklist, contains_pii
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies,
)

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list), 200


@user_bp.route('/me', methods=["GET"])
@jwt_required()
def get_me():
    identity = get_jwt_identity()
    user = User.query.filter_by(user_id=identity).first().to_dict()
    return jsonify(user), 200

@user_bp.route("/<user_uuid>", methods=["GET"])
@jwt_required()
def get_user(user_uuid):
    user = User.query.filter_by(user_id=user_uuid).first()
    if user != None:
        return jsonify(user.to_dict()), 200
    return jsonify({"message":"No such user"}), 404

@user_bp.route('/me', methods=["PUT"])
@jwt_required()
def put_user():
    data = request.get_json()
    identity = get_jwt_identity()
    user = User.query.filter_by(user_id=identity).first()
    name = data["name"]
    if name:
        user.set_name(name)
    surname = data["surname"]
    if surname:
        user.set_surname(surname)
    return jsonify(user.to_dict()), 200
