# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from ..models.admin import Admin
from ..models.stroke import StrokeType, RiskFactor, StrokeManagement, RiskFactorManagement
from ..forms.admin_forms import LoginForm, StrokeTypeForm, RiskFactorForm, StrokeManagementForm, RiskFactorManagementForm
from ..extensions import db
from werkzeug.security import check_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Login and authentication
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        admin_user = Admin.query.filter_by(username=form.username.data).first()
        if admin_user and check_password_hash(admin_user.password, form.password.data):
            login_user(admin_user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password', 'danger')
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

# Dashboard
@admin.route('/')
@login_required
def dashboard():
    stroke_types_count = StrokeType.query.count()
    risk_factors_count = RiskFactor.query.count()
    
    return render_template('admin/dashboard.html', 
                          stroke_types_count=stroke_types_count,
                          risk_factors_count=risk_factors_count)

# Stroke Types CRUD
@admin.route('/stroke-types')
@login_required
def stroke_types():
    stroke_types = StrokeType.query.all()
    return render_template('admin/stroke_types.html', stroke_types=stroke_types)

@admin.route('/stroke-types/add', methods=['GET', 'POST'])
@login_required
def add_stroke_type():
    form = StrokeTypeForm()
    if form.validate_on_submit():
        stroke_type = StrokeType(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(stroke_type)
        db.session.commit()
        flash('Stroke type added successfully!', 'success')
        return redirect(url_for('admin.stroke_types'))
    return render_template('admin/stroke_type_form.html', form=form, title="Add Stroke Type")

@admin.route('/stroke-types/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_stroke_type(id):
    stroke_type = StrokeType.query.get_or_404(id)
    form = StrokeTypeForm(obj=stroke_type)
    
    if form.validate_on_submit():
        stroke_type.name = form.name.data
        stroke_type.description = form.description.data
        db.session.commit()
        flash('Stroke type updated successfully!', 'success')
        return redirect(url_for('admin.stroke_types'))
        
    return render_template('admin/stroke_type_form.html', form=form, title="Edit Stroke Type")

@admin.route('/stroke-types/delete/<int:id>', methods=['POST'])
@login_required
def delete_stroke_type(id):
    stroke_type = StrokeType.query.get_or_404(id)
    try:
        db.session.delete(stroke_type)
        db.session.commit()
        flash('Stroke type deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete stroke type. It may be associated with users or management strategies.', 'danger')
    
    return redirect(url_for('admin.stroke_types'))

# Risk Factors CRUD
@admin.route('/risk-factors')
@login_required
def risk_factors():
    risk_factors = RiskFactor.query.all()
    return render_template('admin/risk_factors.html', risk_factors=risk_factors)

@admin.route('/risk-factors/add', methods=['GET', 'POST'])
@login_required
def add_risk_factor():
    form = RiskFactorForm()
    if form.validate_on_submit():
        risk_factor = RiskFactor(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(risk_factor)
        db.session.commit()
        flash('Risk factor added successfully!', 'success')
        return redirect(url_for('admin.risk_factors'))
    return render_template('admin/risk_factor_form.html', form=form, title="Add Risk Factor")

@admin.route('/risk-factors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_risk_factor(id):
    risk_factor = RiskFactor.query.get_or_404(id)
    form = RiskFactorForm(obj=risk_factor)
    
    if form.validate_on_submit():
        risk_factor.name = form.name.data
        risk_factor.description = form.description.data
        db.session.commit()
        flash('Risk factor updated successfully!', 'success')
        return redirect(url_for('admin.risk_factors'))
        
    return render_template('admin/risk_factor_form.html', form=form, title="Edit Risk Factor")

@admin.route('/risk-factors/delete/<int:id>', methods=['POST'])
@login_required
def delete_risk_factor(id):
    risk_factor = RiskFactor.query.get_or_404(id)
    try:
        db.session.delete(risk_factor)
        db.session.commit()
        flash('Risk factor deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete risk factor. It may be associated with users or management strategies.', 'danger')
    
    return redirect(url_for('admin.risk_factors'))

# Stroke Management CRUD
@admin.route('/stroke-management/<int:stroke_type_id>')
@login_required
def stroke_management(stroke_type_id):
    stroke_type = StrokeType.query.get_or_404(stroke_type_id)
    management_strategies = StrokeManagement.query.filter_by(stroke_type_id=stroke_type_id).all()
    return render_template('admin/stroke_management.html', 
                          stroke_type=stroke_type, 
                          management_strategies=management_strategies)

@admin.route('/stroke-management/add/<int:stroke_type_id>', methods=['GET', 'POST'])
@login_required
def add_stroke_management(stroke_type_id):
    stroke_type = StrokeType.query.get_or_404(stroke_type_id)
    form = StrokeManagementForm()
    
    if form.validate_on_submit():
        management = StrokeManagement(
            stroke_type_id=stroke_type_id,
            description=form.description.data
        )
        db.session.add(management)
        db.session.commit()
        flash('Management strategy added successfully!', 'success')
        return redirect(url_for('admin.stroke_management', stroke_type_id=stroke_type_id))
        
    return render_template('admin/stroke_management_form.html', 
                          form=form, 
                          stroke_type=stroke_type,
                          title="Add Management Strategy")

@admin.route('/stroke-management/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_stroke_management(id):
    management = StrokeManagement.query.get_or_404(id)
    form = StrokeManagementForm(obj=management)
    
    if form.validate_on_submit():
        management.description = form.description.data
        db.session.commit()
        flash('Management strategy updated successfully!', 'success')
        return redirect(url_for('admin.stroke_management', stroke_type_id=management.stroke_type_id))
        
    return render_template('admin/stroke_management_form.html', 
                          form=form, 
                          stroke_type=management.stroke_type,
                          title="Edit Management Strategy")

@admin.route('/stroke-management/delete/<int:id>', methods=['POST'])
@login_required
def delete_stroke_management(id):
    management = StrokeManagement.query.get_or_404(id)
    stroke_type_id = management.stroke_type_id
    
    db.session.delete(management)
    db.session.commit()
    flash('Management strategy deleted successfully!', 'success')
    
    return redirect(url_for('admin.stroke_management', stroke_type_id=stroke_type_id))

# Risk Factor Management CRUD
@admin.route('/risk-factor-management/<int:risk_factor_id>')
@login_required
def risk_factor_management(risk_factor_id):
    risk_factor = RiskFactor.query.get_or_404(risk_factor_id)
    management_strategies = RiskFactorManagement.query.filter_by(risk_factor_id=risk_factor_id).all()
    return render_template('admin/risk_factor_management.html', 
                          risk_factor=risk_factor, 
                          management_strategies=management_strategies)

@admin.route('/risk-factor-management/add/<int:risk_factor_id>', methods=['GET', 'POST'])
@login_required
def add_risk_factor_management(risk_factor_id):
    risk_factor = RiskFactor.query.get_or_404(risk_factor_id)
    form = RiskFactorManagementForm()
    
    if form.validate_on_submit():
        management = RiskFactorManagement(
            risk_factor_id=risk_factor_id,
            description=form.description.data
        )
        db.session.add(management)
        db.session.commit()
        flash('Management strategy added successfully!', 'success')
        return redirect(url_for('admin.risk_factor_management', risk_factor_id=risk_factor_id))
        
    return render_template('admin/risk_factor_management_form.html', 
                          form=form, 
                          risk_factor=risk_factor,
                          title="Add Management Strategy")

@admin.route('/risk-factor-management/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_risk_factor_management(id):
    management = RiskFactorManagement.query.get_or_404(id)
    form = RiskFactorManagementForm(obj=management)
    
    if form.validate_on_submit():
        management.description = form.description.data
        db.session.commit()
        flash('Management strategy updated successfully!', 'success')
        return redirect(url_for('admin.risk_factor_management', risk_factor_id=management.risk_factor_id))
        
    return render_template('admin/risk_factor_management_form.html', 
                          form=form, 
                          risk_factor=management.risk_factor,
                          title="Edit Management Strategy")

@admin.route('/risk-factor-management/delete/<int:id>', methods=['POST'])
@login_required
def delete_risk_factor_management(id):
    management = RiskFactorManagement.query.get_or_404(id)
    risk_factor_id = management.risk_factor_id
    
    db.session.delete(management)
    db.session.commit()
    flash('Management strategy deleted successfully!', 'success')
    
    return redirect(url_for('admin.risk_factor_management', risk_factor_id=risk_factor_id))