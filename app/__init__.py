from flask import Flask
from config import Config
from .extensions import init_extensions
from flask_login import LoginManager
from .routes.main import main as main_blueprint
from .routes.admin import admin as admin_blueprint
from .routes.auth import auth as auth_blueprint  # Add this line
from .models.admin import Admin
from .models.user import User  # Add this line

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    # Check if user is admin or regular user
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_extensions(app)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)  # Add this line
    
    return app