# app/forms/admin_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from ..models.admin import Admin

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class StrokeTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')
    
    def validate_name(self, field):
        from ..models.stroke import StrokeType
        
        # Check if name already exists (for new entries)
        if not hasattr(self, 'id') or not self.id:
            existing = StrokeType.query.filter_by(name=field.data).first()
            if existing:
                raise ValidationError('A stroke type with this name already exists.')

class RiskFactorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')
    
    def validate_name(self, field):
        from ..models.stroke import RiskFactor
        
        # Check if name already exists (for new entries)
        if not hasattr(self, 'id') or not self.id:
            existing = RiskFactor.query.filter_by(name=field.data).first()
            if existing:
                raise ValidationError('A risk factor with this name already exists.')

class StrokeManagementForm(FlaskForm):
    description = TextAreaField('Management Strategy', validators=[DataRequired()])
    submit = SubmitField('Save')

class RiskFactorManagementForm(FlaskForm):
    description = TextAreaField('Management Strategy', validators=[DataRequired()])
    submit = SubmitField('Save')

class AdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Save')
    
    def validate_username(self, field):
        admin = Admin.query.filter_by(username=field.data).first()
        if admin:
            raise ValidationError('Username already exists. Please choose a different one.')