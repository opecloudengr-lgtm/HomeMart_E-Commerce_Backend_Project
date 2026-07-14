from app.extensions import db
from app.models.address import Address

class AddressService:
    @staticmethod
    def get_all_addresses():
        return Address.query.all()

    @staticmethod
    def get_address_by_id(address_id):
        return Address.query.get(address_id)

    @staticmethod
    def create_address(data):
        new_address = Address(**data)
        db.session.add(new_address)
        db.session.commit()
        return new_address

    @staticmethod
    def update_address(address, data):
        for key, value in data.items():
                setattr(address, key, value)
        db.session.commit()
        return address

    @staticmethod
    def delete_address(address):
            db.session.delete(address)
            db.session.commit()