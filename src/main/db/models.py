from src.main.extensions import db, argon2
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


user_group = db.Table(
    'user_group',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.group_id'), primary_key=True)
)

class User(db.Model):
    
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
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

    def set_name(self, name):
        self.name = name

    def set_surname(self, surname):
        self.surname = surname


    def verify_password(self, password):
        return argon2.check_password_hash(self.password_hash, password)

    def validate_email(self):
        try:
            validate_email(self.email)
            return True
        except EmailNotValidError:
            return False

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'surname': self.surname,
            'groups': [group.name for group in self.groups],
            'posts': [post.post_id for post in self.posts],
            'comments': [comment.comment_id for comment in self.comments],
            'ratings': [rating.rating_id for rating in self.ratings],
            'notifications': [notification.notification_id for notification in self.notifications]
        }

class Group(db.Model):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', secondary=user_group, back_populates='groups')
    posts = db.relationship('Post', backref='group', lazy=True)

    def to_dict(self):
        return {
            'group_id': self.group_id,
            'name': self.name,
            'description': self.description,
            'users': [user.user_id for user in self.users],
            'posts': [post.post_id for post in self.posts]
        }

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('Photo', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    ratings = db.relationship('Rating', backref='post', lazy=True)
    notifications = db.relationship('Notification', backref='post', lazy=True)

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'photos': [photo.photo_id for photo in self.photos],
            'comments': [comment.comment_id for comment in self.comments],
            'ratings': [rating.rating_id for rating in self.ratings],
            'notifications': [notification.notification_id for notification in self.notifications]
        }

class Photo(db.Model):
    __tablename__ = 'photos'
    photo_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    base64 = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'photo_id': self.photo_id,
            'post_id': self.post_id,
            'base64': self.base64,
            'created_at': self.created_at
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at
        }

class Rating(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'rating_id': self.rating_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'created_at': self.created_at
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    viewed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'content': self.content,
            'viewed': self.viewed,
            'created_at': self.created_at
        }
