from flask import Flask, jsonify
from src.main.extensions import db, jwt, argon2
from src.main.db.models import User
from src.main.controller.auth import auth_bp

def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    argon2.init_app(app)


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uaim.db'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60
    app.config['JWT_ALGORITHM'] = 'ES256'
    app.config['JWT_PUBLIC_KEY'] = open('ec-pub.key','r').read()
    app.config['JWT_PRIVATE_KEY'] = open('ec.key','r').read()
    app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies"]

    app.register_blueprint(auth_bp)

    register_extensions(app)

    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
