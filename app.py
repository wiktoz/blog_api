from flask import Flask, jsonify
from src.main.extensions import db, jwt, argon2
from src.main.db.models import User
from src.main.controller.AuthController import auth_bp
from src.main.controller.UserController import user_bp
from src.main.controller.GroupController import group_bp

from src.main.db.DatabaseInitializer import DatabaseInitializer

def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    argon2.init_app(app)

def create_app():
    app = Flask(__name__)

    # Konfiguracja aplikacji
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@blog_db:5432/blog'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60
    app.config['JWT_ALGORITHM'] = 'ES256'
    app.config['JWT_PUBLIC_KEY'] = open('ec-pub.key', 'r').read()
    app.config['JWT_PRIVATE_KEY'] = open('ec.key', 'r').read()
    app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    # Rejestracja blueprintów
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(group_bp)


    # Rejestracja rozszerzeń
    register_extensions(app)

    # Tworzenie tabel i inicjalizacja bazy danymi
    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych
        DatabaseInitializer.clear_db()
        DatabaseInitializer.init_db()  # Inicjalizacja bazy danymi

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

