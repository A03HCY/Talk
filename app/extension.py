from flask_sqlalchemy import SQLAlchemy

import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db      = SQLAlchemy()