import configparser
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

config = configparser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

CONFIG_USER_LOGIN = config['users']['user']
CONFIG_USER_PASSWORD = config['users']['password']
CONFIG_DATABASE = config['db']['postgres']

app.config.update(USER_LOGIN=CONFIG_USER_LOGIN, USER_PASSWORD=CONFIG_USER_PASSWORD,
                  SQLALCHEMY_DATABASE_URI=CONFIG_DATABASE)

db = SQLAlchemy(app)

from app.file_server_blueprint import file_server_blueprint
app.register_blueprint(file_server_blueprint, url_prefix='/file_server')
