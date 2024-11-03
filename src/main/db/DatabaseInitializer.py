from src.main.db.models import db, User, Group, Post, Comment, Rating, Notification
from sqlalchemy import text
from datetime import datetime


class DatabaseInitializer:
    @staticmethod
    def init_db():
        # Sprawdzenie, czy dane są już zainicjalizowane, aby uniknąć ponownego dodawania
        if User.query.first():
            print("Database is already initialized.")
            return

        try:
            # Dodanie przykładowych użytkowników
            user1 = User(name='John', surname='Doe', email='john.doe@example.com')
            user1.set_password('password123')

            user2 = User(name='Jane', surname='Smith', email='jane.smith@example.com')
            user2.set_password('securepassword456')

            # Dodanie przykładowych grup
            group1 = Group(name='Home Chefs', description='Group for people who love cooking at home')
            group2 = Group(name='Baking Enthusiasts', description='Group for baking lovers and pastry enthusiasts')

            # Powiązanie użytkowników z grupami
            user1.groups.append(group1)
            user1.groups.append(group2)
            user2.groups.append(group1)

            # Dodanie przykładowych postów
            post1 = Post(title='Welcome to Home Chefs', content='This is a welcome post for all home chefs!',
                         user=user1, group=group1, created_at=datetime.utcnow())
            post2 = Post(title='Baking Tips and Tricks',
                         content='Let’s talk about some awesome baking tips and tricks!', user=user2, group=group2,
                         created_at=datetime.utcnow())

            # Dodanie przykładowych komentarzy
            comment1 = Comment(post=post1, user=user2, content='Thanks for the warm welcome! I love cooking at home!',
                               created_at=datetime.utcnow())
            comment2 = Comment(post=post2, user=user1,
                               content='Great tips! I especially love the one about using cold butter for flaky pastries!',
                               created_at=datetime.utcnow())

            # Dodanie przykładowych ocen
            rating1 = Rating(post=post1, user=user2, rating=5, created_at=datetime.utcnow())
            rating2 = Rating(post=post2, user=user1, rating=4, created_at=datetime.utcnow())

            # Dodanie przykładowych powiadomień
            notification1 = Notification(user=user1, post=post1, content='New comment on your post about home cooking',
                                         viewed=False, created_at=datetime.utcnow())
            notification2 = Notification(user=user2, post=post2, content='Your post was rated 4 stars', viewed=False,
                                         created_at=datetime.utcnow())

            # Dodanie wszystkich obiektów do sesji
            db.session.add_all(
                [user1, user2, group1, group2, post1, post2, comment1, comment2, rating1, rating2, notification1,
                 notification2])

            # Zatwierdzenie zmian w bazie danych
            db.session.commit()
            print("Database has been initialized with sample data.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while initializing the database: {e}")

    @staticmethod
    def clear_db():
        try:
            # Usunięcie powiązań w tabeli pośredniej user_group
            db.session.execute(text('DELETE FROM user_group'))

            # Usunięcie wszystkich danych z tabel w odpowiedniej kolejności, aby uniknąć błędów klucza obcego
            db.session.query(Notification).delete()
            db.session.query(Rating).delete()
            db.session.query(Comment).delete()
            db.session.query(Post).delete()
            db.session.query(User).delete()
            db.session.query(Group).delete()

            # Zatwierdzenie zmian w bazie danych
            db.session.commit()
            print("Database has been cleared.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while clearing the database: {e}")
