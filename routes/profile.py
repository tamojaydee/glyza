from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User
from app import db
from routes.auth import login_required
import logging

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def view_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    return render_template('profile.html', user=user)

@profile_bp.route('/edit', methods=['POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    avatar_url = request.form.get('avatar_url', '').strip()
    bio = request.form.get('bio', '').strip()
    
    # Validation
    if not name or not email:
        flash('Name and email are required.', 'error')
        return redirect(url_for('profile.view_profile'))
    
    # Check if email is already taken by another user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != user_id:
        flash('Email already taken by another user.', 'error')
        return redirect(url_for('profile.view_profile'))
    
    # Update user profile
    user.name = name
    user.email = email
    user.avatar_url = avatar_url if avatar_url else None
    user.bio = bio if bio else None
    
    try:
        db.session.commit()
        flash('Profile updated successfully! 🎭', 'success')
        logging.info(f'Profile updated for user {user_id}')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update profile. Please try again.', 'error')
        logging.error(f'Error updating profile: {str(e)}')
    
    return redirect(url_for('profile.view_profile'))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validation
    if not current_password or not new_password or not confirm_password:
        flash('All password fields are required.', 'error')
        return redirect(url_for('profile.view_profile'))
    
    if not user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('profile.view_profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('profile.view_profile'))
    
    if len(new_password) < 6:
        flash('New password must be at least 6 characters long.', 'error')
        return redirect(url_for('profile.view_profile'))
    
    # Update password
    user.set_password(new_password)
    
    try:
        db.session.commit()
        flash('Password changed successfully! 🔐', 'success')
        logging.info(f'Password changed for user {user_id}')
    except Exception as e:
        db.session.rollback()
        flash('Failed to change password. Please try again.', 'error')
        logging.error(f'Error changing password: {str(e)}')
    
    return redirect(url_for('profile.view_profile'))
