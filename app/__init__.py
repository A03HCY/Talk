from flask import Flask
from app.extension import *
from app.models import *

from app.home import home_blue
from app.auth import auth_blue

import click


def creat_app():
    app = Flask('bbs')

    @app.route('/')
    def index():
        return 'Hello, university bbs'
    return app

def init_example():
    A = User(name='A03')
    B = User(name='Bytes')
    A.set_password('123')
    B.set_password('123')
    db.session.add(A)
    db.session.add(B)
    db.session.commit()


def register_cmd(app: Flask):
    @app.cli.command()
    def resetall():
        click.confirm('Reset the database ?', abort=True)
        db.drop_all()
        db.create_all()
        init_example()
        db.session.commit()


def register_blue(app: Flask):
    db.app = app
    db.init_app(app)
    app.register_blueprint(home_blue)
    app.register_blueprint(auth_blue)


def db_drop_and_create_all(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        init_example()
        db.session.commit()
