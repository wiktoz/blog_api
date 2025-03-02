from flask import request, Response, jsonify, Blueprint, make_response
from src.main.db.models import User
from src.main.extensions import db, jwt, jwt_redis_blocklist, ACCESS_EXPIRES
from src.main.utils.password_validator import is_valid_length, is_on_blacklist, contains_pii
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    get_jwt_identity, set_access_cookies, set_refresh_cookies, 
    unset_jwt_cookies, get_jwt
)
import time

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")



@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    password = data['password']
    email = data['email']
    associated_data = [name,surname,email]
    if not email:
        return jsonify({"message":"Provide email"}), 401
    if not name:
        return jsonify({"message":"Provide your name"}), 401
    if not surname:
        return jsonify({"message":"Provide your surname"}), 401

    if db.session.query(User).filter_by(email=email).first() != None:
        return jsonify({"message":"User with provided email already exist"}), 401
    
    if not is_valid_length(password):
        return jsonify({"message":"Insecure password. Password's length must be in range <8,64>"}), 401
    
    if contains_pii(password, associated_data):
        return jsonify({"message":"Insecure password. Password can't consist of personal information"}), 401
    
    if is_on_blacklist(password):
        return jsonify({"message":"Insecure password. Provided password is compromised"}), 401
    
    user = User(
        email=email,
        name=name,
        surname=surname
    )
    if not user.validate_email():
        return jsonify({"message":"Invalid email"}), 401
    
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except:
        return jsonify({"message":"User with provided email already exist"}), 401
    return jsonify({"message":"Account created"}), 200
    
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    ---
    post:
      summary: User login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        200:
          description: Successful login
          content:
            application/json:
              schema:
                type: object
                properties:
                  login:
                    type: boolean
                  message:
                    type: string
        401:
          description: Invalid credentials
          content:
            application/json:
              schema:
                type: object
                properties:
                  login:
                    type: boolean
                  message:
                    type: string
    """
    data = request.get_json()
    email, password = data["email"], data["password"]
    if not email:
        return jsonify({"login":False,"message":"Provide email"}), 401
    user = db.session.query(User).filter_by(email=email).first()
    if user == None:
        return jsonify({"login":False,"message":"User doesn't exist"}), 401
    if user.verify_password(password):
        token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=email)
        out = jsonify({'login': True})
        set_access_cookies(out,token)
        set_refresh_cookies(out,refresh_token)
        return out, 200
    return jsonify({"login":False,"message":"Invalid credentials"}), 401

@jwt.token_in_blocklist_loader
def is_revoked(jwt_header, jwt_payload: dict):
    """
    Check if the token is revoked.
    ---
    parameters:
      - name: jwt_header
        in: header
        type: string
        required: true
      - name: jwt_payload
        in: body
        schema:
          type: object
          properties:
            jti:
              type: string
    responses:
      200:
        description: Token status
        content:
          application/json:
            schema:
              type: boolean
    """
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@auth_bp.route("/token/revoke/atoken", methods=["POST"])
@jwt_required()
def revoke_access_token():
    """
    Revoke access token.
    ---
    post:
      summary: Revoke access token
      responses:
        200:
          description: Successful revocation
          content:
            application/json:
              schema:
                type: object
                properties:
                  logout:
                    type: boolean
    """
    token = get_jwt()
    jti = token["jti"]
    time_left = token["exp"] - int(time.time())
    jwt_redis_blocklist.set(jti, "", ex=time_left)
    out = jsonify({"logout":True})

    response = make_response(out)
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    return response, 200

@auth_bp.route("/token/revoke/rtoken", methods=["POST"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """
    Revoke refresh token.
    ---
    post:
      summary: Revoke refresh token
      responses:
        200:
          description: Successful revocation
          content:
            application/json:
              schema:
                type: object
                properties:
                  logout:
                    type: boolean
    """
    token = get_jwt()
    jti = token["jti"]
    time_left = token["exp"] - int(time.time())
    jwt_redis_blocklist.set(jti, "", ex=time_left)
    out = jsonify({"logout":True})
    return out, 200


@auth_bp.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh access token.
    ---
    post:
      summary: Refresh access token
      responses:
        200:
          description: Successful token refresh
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    out = jsonify({'access_token': access_token})
    set_access_cookies(out, access_token)
    return out, 200
