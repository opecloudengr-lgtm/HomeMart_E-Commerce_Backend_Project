from flask import Flask, jsonify
from config import Config
from app.extensions import db, migrate, ma, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
  
    from app import models

    from app.routes import (
        auth_bp, superadmin_bp, admin_bp, customer_bp,
        product_bp, cart_bp, wishlist_bp, order_bp, payment_bp,
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(superadmin_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)

    @app.route("/")
    def index():
        return jsonify({
            "message": "Welcome to the HomeMart API",
            "docs": "See README.md for the full list of endpoints",
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "An internal server error occurred"}), 500

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({"error": "Missing authentication token", "detail": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"error": "Invalid authentication token", "detail": reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Your session has expired, please log in again"}), 401

    return app