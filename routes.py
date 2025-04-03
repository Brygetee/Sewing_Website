from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm  # Import the LoginForm class

from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db
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

def patterns():
    return render_template("patterns.html")

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
    return redirect(url_for('home'))

# Protected Dashboard Route
@login_required
def dashboard():
    return render_template("dashboard.html")

# Signup Route
def signup():
    if request.method == 'POST':  # When the form is submitted via POST
        username = request.form.get('username')  # Get the username from the form
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  # Get the password from the form

        # Validation: check if the username or email already exists in the database
        existing_user = User.query.filter_by(email=email).first()  # Query for existing user by email
        if existing_user:
            flash("Email address already in use.", category='error')  # Display error if email is taken
            return redirect(url_for('signup'))  # Redirect back to the signup page

        # Hash the password before saving it in the database
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user and save it to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Commit the changes to the database

        flash("Account created successfully!", category='success')  # Show success message
        return redirect(url_for('login'))  # Redirect to the login page after signup

    return render_template('signup.html')  # If it's a GET request, show the signup form
