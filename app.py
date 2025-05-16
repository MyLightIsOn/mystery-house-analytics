from flask import Flask
from flask_cors import CORS
from config import Config
from database import db
from routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Flask-SQLAlchemy config
    app.config.from_object(Config)

    db.init_app(app)
    register_routes(app)

    return app

app = create_app()
