from flask import Blueprint

advertisement_bp = Blueprint('advertisement', __name__)

from .advertisement_views import *
