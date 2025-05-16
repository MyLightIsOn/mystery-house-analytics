from flask import Flask
from flask_cors import CORS
from config import Config
from database import db
from routes import register_routes
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Flask-SQLAlchemy config
    app.config.from_object(Config)

    db.init_app(app)
    register_routes(app)

    return app

app = create_app()

# Render needs this block to detect an open port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT env var
    app.run(host="0.0.0.0", port=port)        # Host must be 0.0.0.0 to expose externally
