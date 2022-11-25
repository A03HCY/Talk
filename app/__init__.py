from flask          import Flask
from flask_socketio import SocketIO
from app.extension  import *
from app.models     import *

import click

def create_app():
    app = Flask(__name__)
    app.secret_key = '48fj3-2ldjx-c1drl'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.sqlite'
    register_cmd(app)
    register_extensions(app)
    return app

def register_cmd(app: Flask):
    @app.cli.command()
    def resetall():
        click.confirm('Reset the database ?', abort=True)
        db.drop_all()
        db.create_all()
        init_example()
        db.session.commit()

def init_example():
    A = User(name='A03', pswd='123')
    B = User(name='Bytes', pswd='123')
    db.session.add(A)
    db.session.add(B)
    db.session.commit()
    C = Show(hoster=A.id, shown=B.id, redots=0)
    # D = Show(hoster=B.id, shown=A.id, readots=0)
    db.session.add(C)
    # db.session.add(D)
    db.session.commit()


def register_extensions(app:Flask):
    db.init_app(app)