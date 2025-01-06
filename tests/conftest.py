import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.card import Card
from app.models.board import Board
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
def one_saved_board(app):
    board = Board(title="Build a habit of going outside daily", owner="Me")
    db.session.add(board)
    db.session.commit()
    return board

@pytest.fixture
def multiple_boards_with_cards(app):
    board1 = Board(title="Board 1", owner="Owner 1")
    board2 = Board(title="Board 2", owner="Owner 2")
    board3 = Board(title="Board 3", owner="Owner 3")

    card1 = Card(message="Card 1 for Board 1", likes=3, board=board1)
    card2 = Card(message="Card 2 for Board 1", likes=2, board=board1)
    card3 = Card(message="Card 1 for Board 2", likes=5, board=board2)
    card4 = Card(message="Card 1 for Board 3", likes=1, board=board3)

    db.session.add_all([board1, board2, board3, card1, card2, card3, card4])
    db.session.commit()
    
    return [board1, board2, board3]

