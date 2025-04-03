from flask import Flask, redirect, url_for
from models import db
from routes import login_manager, home, login, logout, dashboard, explore, patterns, signup
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

app.config['YOUTUBE_API_KEY'] = os.getenv('YOUTUBE_API_KEY')

# Configurations


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize Extensions database with the flask app
db.init_app(app)
login_manager.init_app(app)


# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create database tables
with app.app_context():
    db.create_all()

# Register Routes
app.add_url_rule('/', 'home', home)
app.add_url_rule('/explore', 'explore', explore)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['POST'])
app.add_url_rule('/signup', 'signup', signup, methods=['GET', 'POST'])
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/patterns', 'patterns', patterns)

if __name__ == '__main__':
    app.run(debug=False)
