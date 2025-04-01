from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import User, db
from forms import LoginForm
import os
import requests

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user by ID from the database

# Home Route

def home():
    return render_template("index.html")

def explore():
    query = request.args.get('query', 'sewing tutorials')  # Default search query
    api_key = os.getenv('YOUTUBE_API_KEY')  # Get API key from .env

    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={api_key}"
    response = requests.get(youtube_url)
    data = response.json()

    print(data)  # DEBUG: Print API response in terminal

    videos = data.get("items", [])  # Extract video list
    return render_template("explore.html", videos=videos)

# Login Route
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):  # Use hashed password check
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template("login.html", form=form)

# Logout Route
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Protected Dashboard Route
@login_required
def dashboard():
    return f"Welcome, {current_user.username}!"
