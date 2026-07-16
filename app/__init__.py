from flask import Flask
from app.config import Config
from app.extensions import db, migrate, ma, jwt
import app.models
from app.routes import home_bp, address_bp, banner_bp, auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(banner_bp)
    app.register_blueprint(auth_bp)

    return app