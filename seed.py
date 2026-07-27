import os
from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models import User, Role

load_dotenv()

app = create_app()

with app.app_context():
    email = os.getenv("SUPER_ADMIN_EMAIL")
    password = os.getenv("SUPER_ADMIN_PASSWORD")
    name = os.getenv("SUPER_ADMIN_NAME")

    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"A user with email '{email}' already exists. Nothing to do.")
    else:
        super_admin = User(name=name, email=email, role=Role.SUPER_ADMIN)
        super_admin.set_password(password)
        db.session.add(super_admin)
        db.session.commit()
        print(f"Super Admin created successfully!")
        print(f"   Email:    {email}")
        print(f"   Password: {password}")
        print("You can now log in with these credentials at POST /auth/login")
