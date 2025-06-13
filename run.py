# Project created by Amr Almehdar in 2025
# Imports
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from extensions import db, bcrypt
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.todo import todo_bp




# Create the Flask application
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = "your_secret_key"  # Replace with a secure key in production

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"  # Location for the SQLite database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking for better performance

# Initialize extensions with the Flask app
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate (app, db)

# Register Blueprints for modular route handling
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(todo_bp, url_prefix='/todo')

# Define the home route
@app.route('/')
def home():
    return render_template('entry_page.html')

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created before starting the app
    app.run(debug=True)
