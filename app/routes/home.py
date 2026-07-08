from flask import Blueprint, jsonify

home_bp=Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def home():
    return jsonify({"success": True, "message": "Welcome to Home Mart"})