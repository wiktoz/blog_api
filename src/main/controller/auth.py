from flask import request, Response, jsonify, Blueprint
from src.main.db.models import User
from src.main.extensions import db, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


def validate_password(password: str, data: list) -> bool:
    if (len(password) < 8 or len(password) > 64):
        return False
    for k in data:
        if (k in password):
            return False
    return True

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    associated_data = [username, email]
    print(associated_data)
    if not username:
        return jsonify('{"message":"Provide username"}'), 200
    if not validate_password(password, associated_data):
        return jsonify('{"message":"Insecure password. Password\'s length must be in range <8,64> and can\'t be weak."}'), 200
    user = User(
        email=email,
        username=username,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify('{"message":"Account created"}'), 200
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username, password = data["username"], data["password"]
    if not username:
        return jsonify('{"message":"Provide username"}'), 200
    user = db.session.query(User).filter_by(username=username).first()
    if user.verify_password(password):
        token = create_access_token(identity=username)
        out = jsonify({"token":token})
        out.set_cookie("token",token,httponly=True)
        return out, 200
    return jsonify('{"message":"Invalid credentials"}'), 200

"""
TODO: Test endpoint, to be removed
"""
@auth_bp.route("/secure", methods=["GET"])
@jwt_required()
def secure():
    subjectUUID = get_jwt_identity()
    return jsonify(logged_in_as=subjectUUID), 200