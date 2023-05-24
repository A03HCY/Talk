from app.extension import *
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True, nullable=False,
                   index=True, autoincrement=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    pswd_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.pswd_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.pswd_hash, password)


class Talk(db.Model):
    __tablename__ = 'talks'
    id = db.Column(db.INTEGER, primary_key=True, nullable=False,
                   index=True, autoincrement=True)
    sender = db.Column(db.INTEGER, nullable=False)
    recver = db.Column(db.INTEGER, nullable=False)
    context = db.Column(db.String(512), nullable=False)
    time = db.Column(db.DATETIME, default=datetime.datetime.now)
