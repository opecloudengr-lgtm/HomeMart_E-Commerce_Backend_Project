from app.extensions import db
from app.models.banner import Banner

class BannerService:
    @staticmethod
    def get_all_banners():
        return Banner.query.all()

    @staticmethod
    def get_banner_by_id(banner_id):
        return Banner.query.get(banner_id)

    @staticmethod
    def create_banner(data):
        new_banner = Banner(**data)
        db.session.add(new_banner)
        db.session.commit()
        return new_banner

    @staticmethod
    def update_banner(banner, data):
        for key, value in data.items():
                setattr(banner, key, value)
        db.session.commit()
        return banner

    @staticmethod
    def delete_banner(banner):
            db.session.delete(banner)
            db.session.commit()