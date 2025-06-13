# Project created by Amr Almehdar in 2025
# todo.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import Todo, User, db, Item
from datetime import datetime
from sqlalchemy import desc

todo_bp = Blueprint('todo', __name__)

# Route for the user dashboard
# Route for the user dashboard
@todo_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')  # Get the logged-in user ID from the session
    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in
    
    todos = Todo.query.filter_by(user_id=user_id).all()  # Fetch to-dos for the user
    # Query the database for the user
    user = User.query.get(user_id)
    return render_template('home.html', todo_lists=todos, username=user.username)



# Route for account info
@todo_bp.route('/account_info', methods=['GET'])
def account_info():
    # Ensure the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in

    # Query the database for the user
    user = User.query.get(user_id)
    if user:
        # Pass the entire user object to the template for better flexibility
        return render_template('account.html', user=user)

    return "User not found", 404


# Home routes

# Route to create a new to-do list
@todo_bp.route('/create', methods=['POST'])
def create():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in

    title = request.form.get('title')
    if title:
        new_list = Todo(title=title, user_id=user_id)
        db.session.add(new_list)
        db.session.commit()
    return redirect(url_for('todo.dashboard'))

# Route to delete a to-do list
@todo_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    lists = Item.query.filter_by(todo_id=id).all()
    for list in lists:
        db.session.delete(list)
    todo_list = Todo.query.get_or_404(id)
    db.session.delete(todo_list)
    db.session.commit()
    return redirect(url_for('todo.dashboard'))



#Route to the indvidual list page
@todo_bp.route('/list/<int:id>', methods=['GET', 'POST'])
def list(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in
    # Fetch the specific to-do list for the user
    todo = Todo.query.filter_by(todo_id=id, user_id=user_id).first()
    if not todo:
        return "To-Do list not found or access denied.", 404  # Handle case where todo doesn't exist or doesn't belong to user
    # Fetch all items associated with this to-do list
    lists = Item.query.filter_by(todo_id=id).all()
    # Pass the todo object and its associated items to the template
    return render_template('list_page.html', todo=todo, lists=lists)



#Route to create a new task
@todo_bp.route('/add_task/<int:id>', methods=['POST'])
def add(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login')) # Redirect to login if not logged in
    task=request.form.get('task')
    urgency = request.form.get('urgency')
    if urgency == "Low Priority":
        urgency_num = 1
    elif urgency == "Medium Priority":
        urgency_num = 2
    else:
        urgency_num = 3
    due_date_str=request.form.get('date')
    # Convert due_date to a Python date object (handle empty strings)
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None
    print(f"VHAT Task: {task}, Urgency: {urgency}, Due Date: {due_date}, Todo ID: {id}")
    if task:
        print(f"Task: {task}, Urgency: {urgency}, Due Date: {due_date}, Todo ID: {id}")
        new_task=Item(task=task, urgency=urgency, urgency_num=urgency_num, due_date=due_date,todo_id=id )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('todo.list', id=id))


#Route to delete and item
@todo_bp.route('/delete-item/<int:id>', methods=['POST'])
def delete_item(id):
    list = Item.query.filter_by(item_id=id).first_or_404()
    todo_id = list.todo_id
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('todo.list', id=todo_id))


#Route to filter the list
@todo_bp.route('/filter/<int:id>', methods=['POST'])
def filter(id):  
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in
    # Fetch the specific to-do list for the user
    todo = Todo.query.filter_by(todo_id=id, user_id=user_id).first()
    if not todo:
        return "To-Do list not found or access denied.", 404  # Handle case where todo doesn't exist or doesn't belong to user
    # Fetch all items associated with this to-do list
    filter = request.form.get('filter')
    if filter == "Priority":
        lists = Item.query.filter_by(todo_id=id).order_by(desc(Item.urgency_num)).all()
    elif filter == "Due":
        lists = Item.query.filter_by(todo_id=id).order_by(Item.due_date).all()
    else:
     lists = Item.query.filter_by(todo_id=id).all()

    
    # Pass the todo object and its associated items to the template
    return render_template('list_page.html', todo=todo, lists=lists)
