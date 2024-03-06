from flask import Flask
from config import Config
from db.DBInterface import DBInterface
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

db = DBInterface()

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(Config)

from app import routes