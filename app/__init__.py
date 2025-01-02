from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models import board, card  # cards_bp
from .routes.card_routes import cards_bp
import os
# Import models, blueprints, and anything else needed to set up the app or database


def create_app(config=None):
    app = Flask(__name__)

    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    # Initialize app with SQLAlchemy db and Migrate

    # Register Blueprints
    # app.register_blueprint(board_bp)
    app.register_blueprint(cards_bp)

    CORS(app)
    return app
