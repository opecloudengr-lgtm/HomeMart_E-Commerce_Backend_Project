from flask import Blueprint, jsonify, request
from app.schemas import address_schema, addresses_schema
from app.services import AddressService

address_bp = Blueprint("address", __name__, url_prefix="/addresses")


@address_bp.get("/")
def get_addresses():
    addresses = AddressService.get_all()
    return jsonify({"success": True, "count": len(addresses), "data": addresses_schema.dump(addresses)})

@address_bp.get("/<int:address_id>")
def get_address(address_id):
    address = AddressService.get_by_id(address_id)
    if not address:
        return jsonify({"success": False, "message": "Address not found." }), 404
    return jsonify({"success": True, "data": address_schema.dump(address)})

@address_bp.post("/")
def create_address():
    data = request.get_json()
    address = AddressService.create(data)
    return jsonify({"success": True, "message": "Address created successfully.", "data": address_schema.dump(address)}), 201


@address_bp.put("/<int:address_id>")
def update_address(address_id):
    address = AddressService.get_by_id(address_id)
    if not address:
        return jsonify({"success": False, "message": "Address not found." }), 404

    data = request.get_json()

    address = AddressService.update(address, data)

    return jsonify({"success": True, "message": "Address updated successfully.", "data": address_schema.dump(address)})


@address_bp.delete("/<int:address_id>")
def delete_address(address_id):
    address = AddressService.get_by_id(address_id)

    if not address:
        return jsonify({"success": False, "message": "Address not found." }), 404

    AddressService.delete(address)

    return jsonify({"success": True, "message": "Address deleted successfully." })