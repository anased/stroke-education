# app/forms/user_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, TelField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, ValidationError
from datetime import date

class UserInfoForm(FlaskForm):
    name = StringField('Tell me your name', validators=[DataRequired(), Length(min=2, max=100)])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()], format='%Y-%m-%d')
    email = EmailField('Email address (optional)', validators=[Optional(), Email()])
    phone = TelField('Phone number (optional)', validators=[Optional(), Length(min=10, max=20)])
    submit = SubmitField('Next: Risk Factors')
    
    def validate_date_of_birth(self, field):
        if field.data > date.today():
            raise ValidationError('Date of birth cannot be in the future')

class RiskFactorsForm(FlaskForm):
    stroke_type = SelectField('Stroke Type', validators=[DataRequired()], 
                            choices=[])
    risk_factors = SelectMultipleField('Have you ever been diagnosed with?', 
                                     choices=[])
    submit = SubmitField("Let's start your journey")

    def __init__(self, *args, **kwargs):
        super(RiskFactorsForm, self).__init__(*args, **kwargs)
        from ..models.stroke import StrokeType, RiskFactor
        
        # Dynamically load choices from database
        stroke_types = StrokeType.query.all()
        risk_factors = RiskFactor.query.all()
        
        self.stroke_type.choices = [(str(st.id), st.name) for st in stroke_types]
        self.risk_factors.choices = [(str(rf.id), rf.name) for rf in risk_factors]
    
    def validate_risk_factors(self, field):
        if len(field.data) > 3:
            raise ValidationError('Please select up to three risk factors')