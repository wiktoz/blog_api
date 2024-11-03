from src.main.extensions import db, argon2
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

Base = declarative_base()

# Definicja tabeli pomocniczej user_group - musi być przed klasami User i Group
user_group = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.group_id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32))
    password_hash = db.Column(db.String, nullable=False)
    groups = db.relationship('Group', secondary=user_group, back_populates='users')
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = argon2.generate_password_hash(password)

    def verify_password(self, password):
        return argon2.check_password_hash(self.password_hash, password)

    def validate_email(self):
        try:
            validate_email(self.email)
            return True
        except EmailNotValidError:
            return False

class Group(db.Model):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', secondary=user_group, back_populates='groups')
    posts = db.relationship('Post', backref='group', lazy=True)

    def __repr__(self):
        return f"Group('{self.name}')"

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('Photo', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    ratings = db.relationship('Rating', backref='post', lazy=True)
    notifications = db.relationship('Notification', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.created_at}')"

class Photo(db.Model):
    __tablename__ = 'photos'
    photo_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    base64 = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Photo('{self.photo_id}', '{self.created_at}')"

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.created_at}')"

class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Rating('{self.rating}', '{self.created_at}')"

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    viewed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Notification('{self.content}', '{self.created_at}')"
