from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Security Features
    role = db.Column(db.String(20), default='user')  # RBAC: 'admin' or 'user'
    totp_secret = db.Column(db.String(32))           # For 2FA
    
    # Audit trail (Track when they joined)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site_name = db.Column(db.String(100), nullable=False)
    site_password_encrypted = db.Column(db.String(500), nullable=False) # In real life, encrypt this!
    strength_score = db.Column(db.Integer) # 0-4 score
