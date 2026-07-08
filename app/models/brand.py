from app.mixins import BaseModel
from app.extensions import db

class Brand(BaseModel):
    __tablename__="brands"

    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Brand {self.name}>"