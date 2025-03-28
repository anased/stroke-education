# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from ..forms.auth_forms import LoginForm, RegistrationForm, SetPasswordForm
from ..extensions import db
from datetime import datetime

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_registered and user.check_password(form.password.data):
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log in user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('auth.dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.is_registered:
            user.set_password(form.password.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user)
            flash('Your account has been created! You are now logged in.', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Registration unsuccessful. Email not found or already registered.', 'danger')
    
    return render_template('auth/register.html', form=form)

@auth.route('/set-password/<token>', methods=['GET', 'POST'])
def set_password(token):
    # This route would be used if we implement email verification
    # For now, we'll use the register route directly
    return redirect(url_for('auth.register'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))