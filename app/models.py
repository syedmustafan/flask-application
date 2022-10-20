from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False, nullable=True)
    password = db.Column(db.String(200), unique=False, nullable=True)
    first_name = db.Column(db.String(200), unique=False, nullable=True)
    last_name = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return '<id {}>'.format(self.username)

    def hashing_password(self, password):
        hashed_password = generate_password_hash(password)
        self.password = hashed_password

    def verify_password(self, password):
        return check_password_hash(self.password, password)
