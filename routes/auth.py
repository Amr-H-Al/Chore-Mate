# Project created by Amr Almehdar in 2025
# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, db

auth_bp = Blueprint('auth', __name__)


# Route for user sign-up
@auth_bp.route('/create', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')  # New field for username
        password = request.form.get('password')

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.signup'))

        # Encrypt password and create new user
        hashed_password = User.hash_password(password)
        new_user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('create.html')

# Route for user login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and User.check_password(user.password, password):
            session['user_id'] = user.uid  # Store user ID in the session
            flash('Login successful.')
            return redirect(url_for('todo.dashboard'))
        flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Route for user logout
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from the session
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))