from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class StrokeEducationForm(FlaskForm):
    stroke_type = SelectField('Stroke Type', validators=[DataRequired()], 
                            choices=[])
    risk_factors = SelectMultipleField('Risk Factors', 
                                     choices=[])
    submit = SubmitField('Get Education Information')

    def __init__(self, *args, **kwargs):
        super(StrokeEducationForm, self).__init__(*args, **kwargs)
        from ..models.stroke import StrokeType, RiskFactor
        
        # Dynamically load choices from database
        stroke_types = StrokeType.query.all()
        risk_factors = RiskFactor.query.all()
        
        self.stroke_type.choices = [(str(st.id), st.name) for st in stroke_types]
        self.risk_factors.choices = [(str(rf.id), rf.name) for rf in risk_factors]
