from flask import Flask
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    with app.app_context():
        from routes.report_routes import report_bp
        app.register_blueprint(report_bp)

    return app
