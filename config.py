import os

class Config:
    # A secret key is used to sign session cookies. In a real app, keep this hidden!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-dev'
    
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False