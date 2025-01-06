from flask import abort, make_response
from ..db import db
import os
import requests


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"model {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()
    model_name = cls.__name__.lower()

    return make_response(new_model.to_dict(), 201)

def send_slack_notification(message):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    
    url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    message_body = {
        "channel": "api-test-channel",
        "text": f"Someone added a new card: {message}"
    }

    requests.post(url, headers=headers, json=message_body)