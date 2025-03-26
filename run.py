from app import create_app
from app.extensions import db
from app.models.stroke import StrokeType, RiskFactor, StrokeManagement, RiskFactorManagement
from app.models.user import User, user_risk_factors
from app.models.admin import Admin
from app.cli import register_commands

app = create_app()
register_commands(app)

@app.cli.command("init-db")
def init_db():
    """Initialize the database with sample data."""
    with app.app_context():
        db.create_all()
        
        # Add sample data if database is empty
        if not StrokeType.query.first():
            # Add stroke types
            ischemic = StrokeType(
                name="Ischemic",
                description="Caused by a blood clot blocking blood flow to the brain"
            )
            db.session.add(ischemic)
            
            hemorrhagic = StrokeType(
                name="Hemorrhagic",
                description="Caused by bleeding in or around the brain"
            )
            db.session.add(hemorrhagic)
            
            tia = StrokeType(
                name="TIA",
                description="Temporary interruption of blood flow to the brain (mini-stroke)"
            )
            db.session.add(tia)
            
            # Add risk factors
            risk_factors_data = [
                ("Hypertension", "High blood pressure"),
                ("Diabetes", "Elevated blood sugar levels"),
                ("Smoking", "Tobacco use"),
                ("High Cholesterol", "Elevated blood cholesterol levels"),
                ("Atrial Fibrillation", "Irregular heart rhythm"),
                ("Obesity", "Body mass index (BMI) of 30 or higher"),
                ("Physical Inactivity", "Lack of regular exercise"),
                ("Family History of Stroke", "Genetic predisposition to stroke")
            ]
            
            for name, desc in risk_factors_data:
                rf = RiskFactor(name=name, description=desc)
                db.session.add(rf)
            
            db.session.commit()
            
            # Add management strategies for stroke types
            ischemic_management = [
                "Blood thinning medications (antiplatelets/anticoagulants)",
                "Blood pressure control",
                "Cholesterol management",
                "Lifestyle modifications"
            ]
            
            for desc in ischemic_management:
                management = StrokeManagement(stroke_type=ischemic, description=desc)
                db.session.add(management)
            
            hemorrhagic_management = [
                "Blood pressure control",
                "Avoid blood thinning medications",
                "Regular monitoring",
                "Lifestyle modifications"
            ]
            
            for desc in hemorrhagic_management:
                management = StrokeManagement(stroke_type=hemorrhagic, description=desc)
                db.session.add(management)
            
            tia_management = [
                "Immediate medical attention",
                "Risk factor modification",
                "Preventive medications",
                "Regular follow-up"
            ]
            
            for desc in tia_management:
                management = StrokeManagement(stroke_type=tia, description=desc)
                db.session.add(management)
            
            # Add management strategies for risk factors
            hypertension = RiskFactor.query.filter_by(name="Hypertension").first()
            hypertension_management = [
                "Regular blood pressure monitoring",
                "Medication adherence",
                "Low-salt diet",
                "Regular exercise",
                "Stress management"
            ]
            
            for desc in hypertension_management:
                management = RiskFactorManagement(risk_factor=hypertension, description=desc)
                db.session.add(management)
                
            # Add management strategies for diabetes
            diabetes = RiskFactor.query.filter_by(name="Diabetes").first()
            diabetes_management = [
                "Regular blood sugar monitoring",
                "Medication or insulin as prescribed",
                "Healthy eating habits",
                "Regular physical activity",
                "Regular foot checks"
            ]
            
            for desc in diabetes_management:
                management = RiskFactorManagement(risk_factor=diabetes, description=desc)
                db.session.add(management)
                
            # Add management strategies for smoking
            smoking = RiskFactor.query.filter_by(name="Smoking").first()
            smoking_management = [
                "Smoking cessation programs",
                "Nicotine replacement therapy",
                "Behavioral counseling",
                "Medication options",
                "Avoid secondhand smoke"
            ]
            
            for desc in smoking_management:
                management = RiskFactorManagement(risk_factor=smoking, description=desc)
                db.session.add(management)
                
            # Add management strategies for high cholesterol
            cholesterol = RiskFactor.query.filter_by(name="High Cholesterol").first()
            cholesterol_management = [
                "Regular cholesterol screening",
                "Heart-healthy diet",
                "Regular exercise",
                "Medication as prescribed",
                "Weight management"
            ]
            
            for desc in cholesterol_management:
                management = RiskFactorManagement(risk_factor=cholesterol, description=desc)
                db.session.add(management)
            
            db.session.commit()
            print("Database initialized with sample data!")

if __name__ == '__main__':
    app.run(debug=True)