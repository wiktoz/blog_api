from flask import request, Response, jsonify, Blueprint
from src.main.db.models import User
from src.main.extensions import db

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    if username and password:
        user = User(
            email=email,
            username=username,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify('{"message":"Account created"}')
    return jsonify('{"message":"Error"}')

