from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #unique identifier
    username = db.Column(db.String(150), unique=True, nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)  # Store hashed passwords

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the hashed password."""
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<User {self.username}>'