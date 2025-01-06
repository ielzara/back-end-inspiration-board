from flask import Blueprint, abort, make_response, request
from app.models.card import Card
from ..db import db
import os
import requests
from .route_utilities import validate_model, create_model

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")


# DELETE
@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    card_message = card.message
    db.session.delete(card)
    db.session.commit()

    return {"details": f'Card {card_id} "{card_message}" successfully deleted'}, 200


# Update Likes
@bp.patch("/<card_id>/like")
def update_card_likes(card_id):
    card = validate_model(Card, card_id)

    card.likes += 1
    db.session.commit()

    return {"card": card.to_dict()}, 200
