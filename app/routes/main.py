# app/routes/main.py
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import current_user, login_user
from ..models.stroke import StrokeType, RiskFactor, StrokeManagement, RiskFactorManagement
from ..models.user import User, user_risk_factors
from ..forms.user_forms import UserInfoForm, RiskFactorsForm
from ..forms.auth_forms import SetPasswordForm
from ..extensions import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
        
    form = UserInfoForm()
    
    if form.validate_on_submit():
        # Store form data in session
        session['user_info'] = {
            'name': form.name.data,
            'date_of_birth': form.date_of_birth.data.strftime('%Y-%m-%d'),
            'email': form.email.data,
            'phone': form.phone.data
        }
        
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and existing_user.is_registered:
            flash('An account with this email already exists. Please log in.', 'info')
            return redirect(url_for('auth.login'))
        
        # Redirect to the next step
        return redirect(url_for('main.risk_factors'))
    
    return render_template('user_info.html', form=form)

@main.route('/risk-factors', methods=['GET', 'POST'])
def risk_factors():
    # Check if user info exists in session
    if 'user_info' not in session:
        flash('Please complete your personal information first', 'warning')
        return redirect(url_for('main.index'))
    
    form = RiskFactorsForm()
    
    if form.validate_on_submit():
        try:
            # Check if a user with this email already exists
            user_data = session.get('user_info')
            existing_user = User.query.filter_by(email=user_data['email']).first()
            
            if existing_user:
                # Update existing user data
                user = existing_user
                user.name = user_data['name']
                user.date_of_birth = datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date()
                user.phone = user_data['phone'] if user_data['phone'] else None
                user.stroke_type_id = int(form.stroke_type.data)
                
                # Update risk factors
                risk_factor_ids = [int(rf_id) for rf_id in form.risk_factors.data]
                risk_factors = RiskFactor.query.filter(RiskFactor.id.in_(risk_factor_ids)).all()
                user.risk_factors = risk_factors
            else:
                # Create a new user
                user = User(
                    name=user_data['name'],
                    date_of_birth=datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date(),
                    email=user_data['email'],
                    phone=user_data['phone'] if user_data['phone'] else None,
                    stroke_type_id=int(form.stroke_type.data)
                )
                
                # Add selected risk factors
                risk_factor_ids = [int(rf_id) for rf_id in form.risk_factors.data]
                risk_factors = RiskFactor.query.filter(RiskFactor.id.in_(risk_factor_ids)).all()
                user.risk_factors = risk_factors
                
                db.session.add(user)
            
            # Save to database
            db.session.commit()
            
            # Store user ID in session for educational content
            session['user_id'] = user.id
            
            # If the user is already registered, log them in
            if user.is_registered:
                login_user(user)
            
            # Clear user info from session
            if 'user_info' in session:
                session.pop('user_info')
            
            # Redirect to educational content
            return redirect(url_for('main.education'))
        except IntegrityError:
            db.session.rollback()
            flash('There was an error with your submission. If you provided an email, it may already be registered.', 'danger')
    
    return render_template('risk_factors.html', form=form)

@main.route('/education')
def education():
    # Check if user exists in session or is logged in
    user_id = session.get('user_id')
    
    if current_user.is_authenticated:
        user = current_user
    elif user_id:
        user = User.query.get_or_404(user_id)
    else:
        flash('Please complete the registration process first', 'warning')
        return redirect(url_for('main.index'))
    
    stroke_type = user.stroke_type
    risk_factors = user.risk_factors
    
    education_data = {
        'user': {
            'name': user.name
        },
        'stroke_info': {
            'name': stroke_type.name,
            'description': stroke_type.description,
            'management': [m.description for m in stroke_type.managements]
        },
        'risk_factor_info': {
            rf.name: {
                'description': rf.description,
                'management': [m.description for m in rf.managements]
            } for rf in risk_factors
        }
    }
    
    # If user is not registered, offer to register
    show_registration = not user.is_registered if user else False
    
    return render_template('education.html', 
                          education_data=education_data,
                          show_registration=show_registration)

@main.route('/register-after-assessment', methods=['GET', 'POST'])
def register_after_assessment():
    # Check if user exists in session
    if 'user_id' not in session:
        flash('Please complete the assessment first', 'warning')
        return redirect(url_for('main.index'))
    
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    
    # If user is already registered, redirect to login
    if user.is_registered:
        flash('You already have an account. Please log in.', 'info')
        return redirect(url_for('auth.login'))
    
    form = SetPasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log in the user
        login_user(user)
        
        flash('Your account has been created! You can now access your education plan anytime.', 'success')
        return redirect(url_for('auth.dashboard'))
    
    return render_template('auth/set_password.html', form=form)

@main.route('/api/stroke-types', methods=['GET'])
def get_stroke_types():
    stroke_types = StrokeType.query.all()
    return jsonify([{
        'id': st.id,
        'name': st.name,
        'description': st.description
    } for st in stroke_types])

@main.route('/api/risk-factors', methods=['GET'])
def get_risk_factors():
    risk_factors = RiskFactor.query.all()
    return jsonify([{
        'id': rf.id,
        'name': rf.name,
        'description': rf.description
    } for rf in risk_factors])