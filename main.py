from flask import Flask
from models import db
from routes import login_manager, home, login, logout, dashboard, explore
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)

app.config['YOUTUBE_API_KEY'] = os.getenv('YOUTUBE_API_KEY')



# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize Extensions
db.init_app(app)
login_manager.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Register Routes
app.add_url_rule('/', 'home', home)
app.add_url_rule('/explore', 'explore', explore)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/dashboard', 'dashboard', dashboard)

if __name__ == '__main__':
    app.run(debug=True)
