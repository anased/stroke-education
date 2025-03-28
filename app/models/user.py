# app/models/user.py
from ..extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Now required
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Added for authentication
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_registered = db.Column(db.Boolean, default=False)  # Flag to indicate if user has set password
    
    # Many-to-many relationship with RiskFactor
    risk_factors = db.relationship('RiskFactor', secondary='user_risk_factors',
                                   backref=db.backref('users', lazy='dynamic'))
    
    # Relationship with StrokeType
    stroke_type_id = db.Column(db.Integer, db.ForeignKey('stroke_type.id'), nullable=True)
    stroke_type = db.relationship('StrokeType', backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.is_registered = True
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

# Association table for User and RiskFactor (unchanged)
user_risk_factors = db.Table('user_risk_factors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('risk_factor_id', db.Integer, db.ForeignKey('risk_factor.id'), primary_key=True)
)