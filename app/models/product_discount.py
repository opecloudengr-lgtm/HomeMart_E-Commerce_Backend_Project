from app.extensions import db

product_discount = db.Table(
"product_discount",
db.Column("product_id",
          db.Integer,
db.ForeignKey("products.id"),
    primary_key=True),
    db.Column("discount_id",
              db.Integer,
db.ForeignKey("discounts.id"),
        primary_key=True))