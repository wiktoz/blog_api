from src.main.db.models import db, User, Group, Post, Comment, Rating, Notification
from sqlalchemy import text
from datetime import datetime
import random
import string


class DatabaseInitializer:
    @staticmethod
    def init_db():
        # Sprawdzenie, czy dane są już zainicjalizowane, aby uniknąć ponownego dodawania
        if User.query.first():
            print("Database is already initialized.")
            return

        try:
            # Dodanie dużej ilości przykładowych danych
            users = []
            groups = []
            posts = []
            comments = []
            ratings = []
            notifications = []

            # Generowanie użytkowników
            email_domains = ["test.com", "test.pl"]
            for i in range(1, 101):  # 100 użytkowników
                email = f"user{i}@{email_domains[i % 2]}"  # Unikalne adresy email
                user = User(name=f'User{i}', surname=f'Surname{i}', email=email)
                user.set_password('password123')
                users.append(user)

            # Dodanie użytkowników do sesji
            db.session.add_all(users)

            # Generowanie grup
            for i in range(1, 21):  # 20 grup
                group = Group(name=f'Group{i}', description=f'This is the description for Group{i}')
                groups.append(group)

            # Dodanie grup do sesji
            db.session.add_all(groups)

            # Powiązanie użytkowników z grupami
            for user in users:
                for _ in range(random.randint(1, 5)):  # Każdy użytkownik jest w 1-5 grupach
                    group = random.choice(groups)
                    if group not in user.groups:
                        user.groups.append(group)

            # Generowanie postów
            for user in users:
                for _ in range(random.randint(1, 10)):  # Każdy użytkownik dodaje 1-10 postów
                    group = random.choice(user.groups)
                    post = Post(
                        title=f'Post by {user.name}',
                        content=f'This is a post by {user.name} in group {group.name}',
                        user=user,
                        group=group,
                        created_at=datetime.utcnow()
                    )
                    posts.append(post)

            # Dodanie postów do sesji
            db.session.add_all(posts)

            # Generowanie komentarzy
            for post in posts:
                for _ in range(random.randint(0, 5)):  # Każdy post ma 0-5 komentarzy
                    user = random.choice(users)
                    comment = Comment(
                        post=post,
                        user=user,
                        content=f'This is a comment by {user.name} on post {post.title}',
                        created_at=datetime.utcnow()
                    )
                    comments.append(comment)

            # Dodanie komentarzy do sesji
            db.session.add_all(comments)

            # Generowanie ocen
            for post in posts:
                for _ in range(random.randint(1, 10)):  # Każdy post ma 1-10 ocen
                    user = random.choice(users)
                    rating = Rating(
                        post=post,
                        user=user,
                        rating=random.randint(1, 5),  # Ocena w zakresie 1-5
                        created_at=datetime.utcnow()
                    )
                    ratings.append(rating)

            # Dodanie ocen do sesji
            db.session.add_all(ratings)

            # Generowanie powiadomień
            for user in users:
                for _ in range(random.randint(1, 5)):  # Każdy użytkownik dostaje 1-5 powiadomień
                    post = random.choice(posts)
                    notification = Notification(
                        user=user,
                        post=post,
                        content=f'You have a new notification about the post "{post.title}"',
                        viewed=random.choice([True, False]),
                        created_at=datetime.utcnow()
                    )
                    notifications.append(notification)

            # Dodanie powiadomień do sesji
            db.session.add_all(notifications)

            # Zatwierdzenie zmian w bazie danych
            db.session.commit()
            print("Database has been initialized with a large set of data.")
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

