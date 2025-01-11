from src.main.db.models import Photo, db, User, Group, Post, Comment, Rating, Notification
from sqlalchemy import text
from datetime import datetime
import random
import base64

class DatabaseInitializer:
    @staticmethod
    def read_image_base64(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

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
            photos = []

            john_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
            john = User(name=john_data["name"], surname=john_data["surname"], email=john_data["email"])
            john.set_password('password123')
            jane = User(name="Jane", surname="Smith", email="jane.smith@example.com")
            jane.set_password('password123')
            db.session.add(john)
            db.session.add(jane)
            db.session.commit()


            # Generowanie użytkowników
            user_data = [
                {"name": "Alice", "surname": "Johnson", "email": "alice.johnson@example.com"},
                {"name": "Bob", "surname": "Brown", "email": "bob.brown@example.com"},
                {"name": "Charlie", "surname": "Davis", "email": "charlie.davis@example.com"},
                {"name": "Diana", "surname": "Miller", "email": "diana.miller@example.com"},
                {"name": "Eve", "surname": "Wilson", "email": "eve.wilson@example.com"},
                {"name": "Frank", "surname": "Moore", "email": "frank.moore@example.com"},
            ]
            for data in user_data:
                user = User(name=data["name"], surname=data["surname"], email=data["email"])
                user.set_password('password123')
                users.append(user)

            # Dodanie użytkowników do sesji
            db.session.add_all(users)


            home_chefs = Group(name="Home Chefs", description="A group for people who love to cook at home.")
            baking_enthusiasts = Group(name="Baking Enthusiasts", description="A group for those who love to bake.")
            db.session.add(home_chefs)
            db.session.add(baking_enthusiasts)
            db.session.commit()
            john.groups.append(home_chefs)
            jane.groups.append(baking_enthusiasts)
            jane.groups.append(home_chefs)
            db.session.commit()

            post1 = Post(title='Welcome to Home Chefs', content='This is a welcome post for all home chefs!',
                         user=john, group=home_chefs, created_at=datetime.utcnow())
            post2 = Post(title='Baking Tips and Tricks',
                         content='Let’s talk about some awesome baking tips and tricks!', user=users[2], group=baking_enthusiasts,
                         created_at=datetime.utcnow())
            # Dodanie przykładowych komentarzy
            comment1 = Comment(post=post1, user=john, content='Thanks for the warm welcome! I love cooking at home!',
                               created_at=datetime.utcnow())
            comment2 = Comment(post=post2, user=john,
                               content='Great tips! I especially love the one about using cold butter for flaky pastries!',
                               created_at=datetime.utcnow())
            # Dodanie przykładowych ocen
            rating1 = Rating(post=post1, user=john, rating=5, created_at=datetime.utcnow())
            rating2 = Rating(post=post2, user=jane, rating=4, created_at=datetime.utcnow())
            # Dodanie przykładowych powiadomień
            notification1 = Notification(user=john, post=post1, content='New comment on your post about home cooking',
                                         viewed=False, created_at=datetime.utcnow())
            notification2 = Notification(user=jane, post=post2, content='Your post was rated 4 stars', viewed=False,
                                         created_at=datetime.utcnow())
            # Dodanie wszystkich obiektów do sesji
            db.session.add_all(
                [post1, post2, comment1, comment2, rating1, rating2, notification1,
                 notification2])
            # Zatwierdzenie zmian w bazie danych
            db.session.commit()


            group_data = [
                {"name": "Culinary Enthusiasts", "description": "A group for those who love to cook and share recipes."},
                {"name": "Healthy Eaters", "description": "A group focused on healthy eating and nutritious recipes."},
                {"name": "Baking Lovers", "description": "A group for people who enjoy baking and sharing their baked goods."},
                {"name": "Food Critics", "description": "A group for those who love to review and critique different foods."}
            ]
            
            for data in group_data:
                group = Group(name=data["name"], description=data["description"])
                groups.append(group)

            # Dodanie grup do sesji
            db.session.add_all(groups)

            # Powiązanie użytkowników z grupami
            for user in users:
                for _ in range(random.randint(1, 3)):  # Każdy użytkownik jest w 1-2 grupach
                    group = random.choice(groups)
                    if group not in user.groups:
                        user.groups.append(group)

            # Generowanie postów
            image_files = [
                "src/main/db/images/1.jpg",
                "src/main/db/images/2.jpg",
                "src/main/db/images/3.jpg"
            ]

            image_data_list = [DatabaseInitializer.read_image_base64(file) for file in image_files]

            post_titles = [
                "Delicious Finger Foods",
                "Homemade Soups",
                "Gourmet Desserts",
                "Healthy Salads",
                "Quick and Easy Dinners",
                "Baking Bread at Home",
                "Exotic Spices",
                "Vegetarian Delights",
                "Seafood Specialties",
                "Comfort Food Classics"
            ]

            for i in range(46):
                user = random.choice(users)
                group = random.choice(user.groups)
                post_title = random.choice(post_titles)
                post = Post(
                    title=post_title, 
                    content=f'This is a culinary post by {user.name} in group {group.name}',
                    user=user,
                    group=group,
                    created_at=datetime.utcnow()
                )
                posts.append(post)

                # Create and bind photos to the post
                image_data = image_data_list[i % len(image_data_list)]
                photo = Photo(
                    post=post,
                    base64=image_data,
                    created_at=datetime.utcnow()
                )
                photos.append(photo)

            # Dodanie postów i zdjęć do sesji
            db.session.add_all(posts)
            db.session.add_all(photos)

            comment_contents = [
                "This looks delicious!",
                "I can't wait to try this recipe.",
                "Thanks for sharing!",
                "Yummy!",
                "This is amazing!",
                "Great post!",
                "I love this!",
                "So tasty!",
                "Fantastic recipe!",
                "Looks great!"
            ]

            for post in posts:
                for _ in range(random.randint(0, 3)):  # Każdy post ma 0-3 komentarzy
                    user = random.choice(users)
                    comment_content = random.choice(comment_contents)
                    comment = Comment(
                        post=post,
                        user=user,
                        content=comment_content,
                        created_at=datetime.utcnow()
                    )
                    comments.append(comment)

            # Dodanie komentarzy do sesji
            db.session.add_all(comments)

            # Generowanie ocen
            for post in posts:
                for _ in range(random.randint(1, 5)):  # Każdy post ma 1-5 ocen
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
                for _ in range(random.randint(1, 3)):  # Każdy użytkownik dostaje 1-3 powiadomień
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
            db.session.query(Photo).delete()
            db.session.query(Post).delete()
            db.session.query(User).delete()
            db.session.query(Group).delete()

            # Zatwierdzenie zmian w bazie danych
            db.session.commit()
            print("Database has been cleared.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while clearing the database: {e}")

