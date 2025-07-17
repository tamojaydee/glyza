from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User
from app import db
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}! 🥞', 'success')
            logging.info(f'User {username} logged in successfully')
            return redirect(url_for('workflow.dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            logging.warning(f'Failed login attempt for username: {username}')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            logging.info('Registration attempt started')
            
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            logging.info(f'Registration data: username={username}, email={email}, password_length={len(password)}')
            
            # Validation
            if not username or not email or not password:
                logging.warning('Missing required fields')
                flash('Please fill in all required fields.', 'error')
                return render_template('register.html')
            
            if password != confirm_password:
                logging.warning('Password mismatch')
                flash('Passwords do not match.', 'error')
                return render_template('register.html')
            
            if len(password) < 6:
                logging.warning('Password too short')
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('register.html')
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                logging.warning(f'Username {username} already exists')
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('register.html')
            
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                logging.warning(f'Email {email} already registered')
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('register.html')
            
            # Create new user
            logging.info('Creating new user')
            user = User(username=username, email=email, name=username)
            user.set_password(password)
            
            logging.info('Adding user to database')
            db.session.add(user)
            db.session.commit()
            logging.info('User committed to database successfully')
            
            # Auto-login after registration
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Registration successful! Welcome to Pancake Cinema Workflows, {username}! 🎬🥞', 'success')
            logging.info(f'New user registered successfully: {username} (ID: {user.id})')
            return redirect(url_for('workflow.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f'Registration error: {str(e)}', exc_info=True)
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! See you at the next show! 🎬', 'info')
    return redirect(url_for('auth.login'))

def login_required(f):
    """Decorator to require login for protected routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
