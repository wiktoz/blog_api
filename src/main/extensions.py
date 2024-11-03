from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_argon2 import Argon2

db = SQLAlchemy()
jwt = JWTManager()
argon2 = Argon2()


