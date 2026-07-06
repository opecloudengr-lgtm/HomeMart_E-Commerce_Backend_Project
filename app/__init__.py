# Application factory
from flask import Flask
from .config import Config
from .extensions import db, migrate, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    @app.route('/')
    def index():
        return {"success": True, "message": "Welcome to the HomeMart E-Commerce Backend!"}
    return app