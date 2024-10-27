from flask import Flask
from flask_cors import CORS
from py_eureka_client import eureka_client

from .config import EUREKA_SERVER
from .database import db
from .routes.advertisement_views import advertisement_bp


def create_app():

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    eureka_client.init(eureka_server=EUREKA_SERVER,
                       app_name="advertisement",
                       instance_id="advertisement-instance",
                       instance_port=5000,
                       instance_host="127.0.0.1")

    db.init_app(app)
    app.debug = True

    CORS(app, resources={r"/api/advertisement/*": {"origins": "*", "methods": ["GET", "POST", "DELETE"]}})

    with app.app_context():
        db.create_all()

    app.register_blueprint(advertisement_bp)
    return app
