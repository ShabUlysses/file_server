from flask import Blueprint

file_server_blueprint = Blueprint('file_server_blueprint', __name__)

from . import views
