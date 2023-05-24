from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db = SQLAlchemy()
manager = LoginManager()
