from src.main.db.models import db, User, Group, Post, Comment, Rating, Notification
from datetime import datetime

class DatabaseInitializer:
    @staticmethod
    def init_db():
        # Sprawdzenie, czy dane są już zainicjalizowane, aby uniknąć ponownego dodawania
        if User.query.first():
            print("Database is already initialized.")
            return

        # Dodanie przykładowych użytkowników
        user1 = User(name='John', surname='Doe', email='john.doe@example.com')
        user1.set_password('password123')

        try:
            db.session.commit()
            print("Database has been initialized with sample data.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while initializing the database: {e}")
