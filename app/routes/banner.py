from flask import Blueprint, jsonify, request

from app.schemas import banner_schema, banners_schema
from app.services import BannerService

banner_bp = Blueprint("banner", __name__, url_prefix="/banners")

@banner_bp.get("/")
def get_banners():
    banners = BannerService.get_all()

    return jsonify({"success": True, "count": len(banners), "data": banners_schema.dump(banners)})


@banner_bp.get("/<int:banner_id>")
def get_banner(banner_id):
    banner = BannerService.get_by_id(banner_id)

    if not banner:
        return jsonify({"success": False, "message": "Banner not found."}), 404

    return jsonify({"success": True, "data": banner_schema.dump(banner)})


@banner_bp.post("/")
def create_banner():
    data = request.get_json()

    banner = BannerService.create(data)

    return jsonify({"success": True, "message": "Banner created successfully.", "data": banner_schema.dump(banner)}), 201


@banner_bp.put("/<int:banner_id>")
def update_banner(banner_id):
    banner = BannerService.get_by_id(banner_id)

    if not banner:
        return jsonify({"success": False, "message": "Banner not found."}), 404

    data = request.get_json()

    banner = BannerService.update(banner, data)

    return jsonify({"success": True, "message": "Banner updated successfully.", "data": banner_schema.dump(banner)})


@banner_bp.delete("/<int:banner_id>")
def delete_banner(banner_id):
    banner = BannerService.get_by_id(banner_id)

    if not banner:
        return jsonify({"success": False, "message": "Banner not found." }), 404

    BannerService.delete(banner)
    return jsonify({"success": True, "message": "Banner deleted successfully." })