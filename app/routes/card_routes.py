from flask import Blueprint, abort, make_response, request
from app.models.card import Card
from ..db import db
import os
import requests
from .route_utilities import validate_model, create_model

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.post("")
def create_card():

    request_body = request.get_json()

    # Check for required fields before calling create_model
    if "message" not in request_body or "count" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    response = create_model(Card, request_body)
    card_dict = response.get_json()
    return make_response({"Card": card_dict}, 201)

    
@bp.get("")
def get_all_cards():
    query = db.select(Card).order_by(Card.id)
    cards = db.session.scalars(query)
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    cards_response = []
    for card in cards:
        cards_response.append(
            {
                "id": card.id,
                "message": card.message,
                "count": card.count
            }
        )
    return cards_response

@bp.get("/<card_id>")
def get_one_card(card_id):
    query = db.select(Card).where(Card.id == card_id)
    card = db.session.scalar(query)

    card = validate_model(Card, card_id)
    return {"card": card.to_dict()}, 200

# DELETE
@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    card_message = card.message
    db.session.delete(card)
    db.session.commit()

    return {"details": f'Card {card_id} "{card_message}" successfully deleted'}, 200

