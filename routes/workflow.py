from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import User, Task
from app import db
from routes.auth import login_required
from datetime import datetime
import logging

workflow_bp = Blueprint('workflow', __name__)

@workflow_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Get tasks with filters
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '').strip()
    
    tasks_query = Task.query.filter_by(user_id=user_id)
    
    if status_filter != 'all':
        tasks_query = tasks_query.filter_by(status=status_filter)
    
    if search_query:
        tasks_query = tasks_query.filter(Task.title.contains(search_query))
    
    tasks = tasks_query.order_by(Task.created_at.desc()).all()
    
    # Get task counts for dashboard stats
    total_tasks = Task.query.filter_by(user_id=user_id).count()
    pending_tasks = Task.query.filter_by(user_id=user_id, status='pending').count()
    in_progress_tasks = Task.query.filter_by(user_id=user_id, status='in-progress').count()
    done_tasks = Task.query.filter_by(user_id=user_id, status='done').count()
    
    stats = {
        'total': total_tasks,
        'pending': pending_tasks,
        'in_progress': in_progress_tasks,
        'done': done_tasks
    }
    
    return render_template('dashboard.html', 
                         user=user, 
                         tasks=tasks, 
                         stats=stats,
                         current_filter=status_filter,
                         search_query=search_query)

@workflow_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    user_id = session['user_id']
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'medium')
    due_date_str = request.form.get('due_date', '')
    
    if not title:
        flash('Task title is required.', 'error')
        return redirect(url_for('workflow.dashboard'))
    
    # Parse due date if provided
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid due date format.', 'error')
            return redirect(url_for('workflow.dashboard'))
    
    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        user_id=user_id
    )
    
    try:
        db.session.add(task)
        db.session.commit()
        flash(f'Task "{title}" added successfully! 🎬', 'success')
        logging.info(f'Task created by user {user_id}: {title}')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add task. Please try again.', 'error')
        logging.error(f'Error adding task: {str(e)}')
    
    return redirect(url_for('workflow.dashboard'))

@workflow_bp.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('workflow.dashboard'))
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    status = request.form.get('status', task.status)
    priority = request.form.get('priority', task.priority)
    due_date_str = request.form.get('due_date', '')
    
    if not title:
        flash('Task title is required.', 'error')
        return redirect(url_for('workflow.dashboard'))
    
    # Parse due date if provided
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid due date format.', 'error')
            return redirect(url_for('workflow.dashboard'))
    
    # Update task
    task.title = title
    task.description = description
    task.status = status
    task.priority = priority
    task.due_date = due_date
    task.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash(f'Task "{title}" updated successfully! 🎭', 'success')
        logging.info(f'Task {task_id} updated by user {user_id}')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update task. Please try again.', 'error')
        logging.error(f'Error updating task: {str(e)}')
    
    return redirect(url_for('workflow.dashboard'))

@workflow_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('workflow.dashboard'))
    
    task_title = task.title
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash(f'Task "{task_title}" deleted successfully! 🗑️', 'success')
        logging.info(f'Task {task_id} deleted by user {user_id}')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete task. Please try again.', 'error')
        logging.error(f'Error deleting task: {str(e)}')
    
    return redirect(url_for('workflow.dashboard'))

# RESTful API endpoints
@workflow_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks_api():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks])

@workflow_bp.route('/api/tasks', methods=['POST'])
@login_required
def create_task_api():
    user_id = session['user_id']
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        user_id=user_id
    )
    
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create task'}), 500

@workflow_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task_api(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task.to_dict())

@workflow_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task_api(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task.title = data['title']
    task.description = data.get('description', '')
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500

@workflow_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task_api(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task'}), 500
