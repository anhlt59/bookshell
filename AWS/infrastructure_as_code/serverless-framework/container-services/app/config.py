"""Default configuration

Use env var to override
"""
import os

DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY", "1234567890")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///local.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
