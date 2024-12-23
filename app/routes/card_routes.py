from flask import Blueprint, abort, make_response, request, Response
from app.models.card import Card
import os
import requests
from ..db import db
from .route_utilities import validate_model, create_model