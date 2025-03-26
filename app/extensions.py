from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    csrf.init_app(app)