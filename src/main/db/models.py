from src.main.extensions import db, argon2


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = argon2.generate_password_hash(password)
    
    def verify_password(self, password):
        return argon2.check_password_hash(self.password_hash,password)

    