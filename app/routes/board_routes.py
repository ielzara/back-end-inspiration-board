from flask import Blueprint, abort, make_response, request, Response
from app.models.board import Board
from app.models.card import Card
import os
import requests
from ..db import db
from .route_utilities import validate_model, create_model, send_slack_notification

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# Create a new board
@bp.post("")
def create_board():
    request_body = request.get_json()
    response = create_model(Board, request_body)
    board_dict = response.get_json()

    return make_response({"board": board_dict}), 201

# Get all boards
@bp.get("")
def get_all_boards():
    query = db.select(Board)
    query = query.order_by(Board.id)
    boards = db.session.execute(query).scalars().all() 
    boards_dict = [board.to_dict() for board in boards]

    return make_response({"boards": boards_dict})

# Get a single board
@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    
    return {"board": board.to_dict()}, 200

# Update a board
@bp.put("/<board_id>")
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    board.title = request_body["title"]
    board.owner = request_body["owner"]
    db.session.commit()

    return {"board": board.to_dict()}, 200


# Delete a board
@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)
    board_title = board.title
    db.session.delete(board)
    db.session.commit()

    return {"details": f'Board {board_id} "{board_title} successfully deleted'}, 200

# Get all cards for a board
@bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)

    return{
        "id": board.id,
        "title": board.title,
        "owner": board.owner,
        "cards": [card.to_dict() for card in board.cards],
    }

# Add a card to a board
@bp.post("/<board_id>/cards")
def handle_cards_for_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    if "card_ids" in request_body:
        card_ids = request_body["card_ids"]
        for card_id in card_ids:
            card = validate_model(Card, card_id)
            if card not in board.cards:
                board.cards.append(card)
        db.session.commit()
        return { "id": board.id, "card_ids": [card.id for card in board.cards] }, 200
    else:
        request_body["board_id"] = board.id
        
        send_slack_notification(request_body["message"])
        
        return create_model(Card, request_body)