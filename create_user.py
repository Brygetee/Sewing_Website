from main import app
from models import db, User
from werkzeug.security import generate_password_hash
import os
db.drop_all()
db.create_all()

def create_test_user():
    with app.app_context():  # Make sure you're in the app context
        # Drop existing tables if any
        db.drop_all()

        # Recreate tables (this will now match the updated schema)
        db.create_all()

        # Check if the admin user exists
        existing_user = User.query.filter_by(username=os.getenv('TESTER_USERNAME').first()
        if existing_user:
            print("Test user already exists.")
            return

        # Create a new admin user with hashed password
        new_user = User(username=os.getenv('TESTER_USERNAME'), email=os.getenv('TESTER_EMAIL'))
        new_user.password_hash = generate_password_hash("password")
        db.session.add(new_user)
        db.session.commit()

        print("Test user created successfully!")

if __name__ == "__main__":
    create_test_user()
