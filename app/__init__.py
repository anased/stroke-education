from flask import Flask
from config import Config
from .extensions import init_extensions
from flask_login import LoginManager
from .routes.main import main as main_blueprint
from .routes.admin import admin as admin_blueprint  # Add this line
from .models.admin import Admin  # Add this line

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_extensions(app)
    login_manager.init_app(app)  # Add this line
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)  # Add this line
    
    return app