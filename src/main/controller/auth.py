from flask import request, Response, jsonify, Blueprint
from src.main.db.models import User
from src.main.extensions import db, jwt
from src.main.utils.password_validator import is_valid_length, is_on_blacklist, contains_pii
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")



@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data['name']
    surname = data['name']
    password = data['password']
    email = data['email']
    associated_data = [name,surname,email]
    if not email:
        return jsonify('{"message":"Provide email"}'), 200
    if not is_valid_length(password):
        return jsonify({"message":"Insecure password. Password's length must be in range <8,64>"}), 200
    if contains_pii(password, associated_data):
        return jsonify({"message":"Insecure password. Password can't consist of personal information"}), 200
    if is_on_blacklist(password):
        return jsonify({"message":"Insecure password. Provided password is compromised"}), 200
    user = User(
        email=email,
        name=name,
        surname=surname
    )
    if db.session.query(User).filter_by(email=email).first() != None:
        return jsonify('{"message":"User with provided email already exist"}'), 200
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except:
        return jsonify('{"message":"User with provided email already exist"}'), 200
    return jsonify('{"message":"Account created"}'), 200
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data["email"], data["password"]
    if not email:
        return jsonify({"login":False,"message":"Provide email"}), 200
    user = db.session.query(User).filter_by(email=email).first()
    if user == None:
        return jsonify({"login":False,"message":"User doesn't exist"}), 200
    if user.verify_password(password):
        token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        out = jsonify({'login': True})
        set_access_cookies(out,token)
        set_refresh_cookies(out,refresh_token)
        return out, 200
    return jsonify({"login":False,"message":"Invalid credentials"}), 200



"""
TODO: Test endpoint, to be removed
"""
@auth_bp.route("/secure", methods=["GET"])
@jwt_required()
def secure():
    subjectUUID = get_jwt_identity()
    return jsonify(logged_in_as=subjectUUID), 200

@auth_bp.route("/secure2", methods=["POST"])
@jwt_required()
def secure2():
    data = request.get_json()
    test = data["test"]
    return jsonify(test), 200