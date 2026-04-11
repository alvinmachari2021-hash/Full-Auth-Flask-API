import os

class Config:
    # Used for signing session cookies
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    # Database connection
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///repcount.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False