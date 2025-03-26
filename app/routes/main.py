# app/routes/main.py
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from ..models.stroke import StrokeType, RiskFactor, StrokeManagement, RiskFactorManagement
from ..models.user import User, user_risk_factors
from ..forms.user_forms import UserInfoForm, RiskFactorsForm
from ..extensions import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError  # Add this import

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = UserInfoForm()
    
    if form.validate_on_submit():
        # Store form data in session
        session['user_info'] = {
            'name': form.name.data,
            'date_of_birth': form.date_of_birth.data.strftime('%Y-%m-%d'),
            'email': form.email.data,
            'phone': form.phone.data
        }
        
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
            # Create a new user
            user_data = session.pop('user_info')
            
            # Handle empty email and phone by setting to None
            email = user_data['email'] if user_data['email'] else None
            phone = user_data['phone'] if user_data['phone'] else None
            
            user = User(
                name=user_data['name'],
                date_of_birth=datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date(),
                email=email,  # Use None instead of empty string
                phone=phone,  # Use None instead of empty string
                stroke_type_id=int(form.stroke_type.data)
            )
            
            # Add selected risk factors
            risk_factor_ids = [int(rf_id) for rf_id in form.risk_factors.data]
            risk_factors = RiskFactor.query.filter(RiskFactor.id.in_(risk_factor_ids)).all()
            user.risk_factors = risk_factors
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Store user ID in session for educational content
            session['user_id'] = user.id
            
            # Redirect to educational content
            return redirect(url_for('main.education'))
        except IntegrityError:
            db.session.rollback()
            flash('There was an error with your submission. If you provided an email, it may already be registered.', 'danger')
    
    return render_template('risk_factors.html', form=form)

@main.route('/education')
def education():
    # Check if user exists in session
    if 'user_id' not in session:
        flash('Please complete the registration process first', 'warning')
        return redirect(url_for('main.index'))
    
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    
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
    
    return render_template('education.html', education_data=education_data)

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