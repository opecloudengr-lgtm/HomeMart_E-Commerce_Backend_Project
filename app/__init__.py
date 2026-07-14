# Application factory
from flask import Flask, app
from app.config import Config
from app.extensions import db, migrate, ma
import app.models
from app.routes import home_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    app.register_blueprint(home_bp)
    return app