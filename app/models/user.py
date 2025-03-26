# app/models/user.py
from ..extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with RiskFactor
    risk_factors = db.relationship('RiskFactor', secondary='user_risk_factors',
                                   backref=db.backref('users', lazy='dynamic'))
    
    # Relationship with StrokeType
    stroke_type_id = db.Column(db.Integer, db.ForeignKey('stroke_type.id'), nullable=True)
    stroke_type = db.relationship('StrokeType', backref=db.backref('users', lazy=True))

# Association table for User and RiskFactor
user_risk_factors = db.Table('user_risk_factors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('risk_factor_id', db.Integer, db.ForeignKey('risk_factor.id'), primary_key=True)
)