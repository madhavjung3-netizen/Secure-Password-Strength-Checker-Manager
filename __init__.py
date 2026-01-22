from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' # Redirect here if not logged in

    # --- FIX: Define the user_loader ---
    # This tells Flask-Login how to find a specific user from the ID stored in the session cookie
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -----------------------------------

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all() # Creates the database file automatically

    return app