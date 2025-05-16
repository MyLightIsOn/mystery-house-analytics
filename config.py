import os

# Load environment variable for database connection
DATABASE_URL = os.getenv("DATABASE_URL")

class Config:
    # Core Flask config
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False