from app.mixins import BaseModel
from app.extensions import db


class Banner(BaseModel):
    __tablename__="banners"

    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Banner{self.title}>"