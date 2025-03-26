from ..extensions import db
from datetime import datetime

class StrokeType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    managements = db.relationship('StrokeManagement', backref='stroke_type', lazy=True)

class RiskFactor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    managements = db.relationship('RiskFactorManagement', backref='risk_factor', lazy=True)

class StrokeManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stroke_type_id = db.Column(db.Integer, db.ForeignKey('stroke_type.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RiskFactorManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    risk_factor_id = db.Column(db.Integer, db.ForeignKey('risk_factor.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)