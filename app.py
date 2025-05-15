from flask import Flask
from flask_cors import CORS
from database import get_connection
from routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("config")

    register_routes(app)

    return app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
