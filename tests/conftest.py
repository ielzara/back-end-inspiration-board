import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.card import Card
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    dream_card = Card(message="Living in the clouds with no insects",
                    likes=5)
    realistic_card = Card(count="Gotta finish this card",
                        likes=1)

    db.session.add_all([dream_card, realistic_card])
    db.session.commit()