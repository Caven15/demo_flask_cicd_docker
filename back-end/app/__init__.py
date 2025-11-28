from flask import Flask
from app.routes import init_routes
from flask_cors import CORS
from app.tools.middlewares.request_logging import register_request_logging

def create_app() -> Flask:
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    init_routes(app)
    register_request_logging(app)
    return app
