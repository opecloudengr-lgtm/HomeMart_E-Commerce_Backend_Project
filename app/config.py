import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f"sqlite:///{os.path.join(BASE_DIR, 'homemart.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False