from flask import Flask
from config import Config
from DBInterface import DBInterface
from flask_login import LoginManager

app = Flask(__name__)

db = DBInterface()

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(Config)

from app import routes