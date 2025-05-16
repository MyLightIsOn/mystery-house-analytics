from .log_routes import log_bp
from .feedback_routes import feedback_bp
from .analytics_routes import analytics_bp

# Central function to register all blueprints
def register_routes(app):
    app.register_blueprint(log_bp, url_prefix="/api")
    app.register_blueprint(feedback_bp, url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api")
