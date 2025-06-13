# Project created by Amr Almehdar in 2025
# models.py
from extensions import db, bcrypt
from datetime import date

# User model for storing user data
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Added username field for login
    password = db.Column(db.String(200), nullable=False)  # Hashed password

    # Utility method to hash a password
    @staticmethod
    def hash_password(plain_text_password):
        return bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Utility method to verify a hashed password
    @staticmethod
    def check_password(hashed_password, plain_text_password):
        return bcrypt.check_password_hash(hashed_password, plain_text_password)

# Todo model for managing to-do list entries
class Todo(db.Model):
    todo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)  # Foreign key to associate with User
    user = db.relationship('User', backref=db.backref('todos', lazy=True))


#Todo model for managing each item in list
class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(100), nullable=False, default="To be filled")
    urgency = db.Column(db.String(20), nullable=False, default="Low")
    urgency_num = db.Column(db.Integer, default=1)
    due_date=db.Column(db.Date, default=date.today, nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.todo_id'), nullable=False) #Foriegn Key to associate with todo
    todo = db.relationship('Todo', backref=db.backref('items', lazy=True))

