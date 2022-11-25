from flask_socketio import Namespace, emit
from flask          import request, session
from app.extension  import *
from sqlalchemy     import or_, and_

import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False, unique=True, comment='user nick name')
    pswd = db.Column(db.String(256), comment='user password')

    visible = db.Column(db.String(4), default='')

    current = db.Column(db.String(32), default='')


class Talk(db.Model):
    __tablename__ = 'talks'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)

    sender  = db.Column(db.INTEGER, nullable=False)
    recver  = db.Column(db.INTEGER, nullable=False)
    context = db.Column(db.String(512), nullable=False)
    time    = db.Column(db.DATETIME, default=datetime.datetime.now)


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)

    hoster = db.Column(db.INTEGER, nullable=False)
    shown  = db.Column(db.INTEGER, nullable=False)
    redots = db.Column(db.INTEGER, default=0)


class Extension:

    @staticmethod
    def Containshown(data, uid:int) -> bool:
        for i in data:
            if i.shown == uid: return True
        return False

    @staticmethod
    def Has(uid:int) -> bool:
        exa = User.query.filter_by(id=uid).first()
        if exa: return True
        return False

    @staticmethod
    def Getbyname(name:str) -> User:
        exa = User.query.filter_by(name=name).first()
        return exa
    
    @staticmethod
    def Getbyid(uid:int) -> User:
        exa = User.query.filter_by(id=uid).first()
        return exa
    
    @staticmethod
    def Auth(name:str, pswd:str) -> bool:
        exa = User.query.filter_by(name=name).first()
        if not exa: return False
        if exa.pswd != pswd: return False
        return True
    
    @staticmethod
    def Listbyid(uid:int) -> list:
        alls = Show.query.filter_by(hoster=uid).all()
        if not alls: return []
        return alls
    
    @staticmethod
    def Listbyname(name:str) -> list:
        exa = Extension.Getbyname(name)
        if not exa: return []
        return Extension.Listbyid(exa.id)
    
    @staticmethod
    def Talksender(uid:int) -> list:
        alls = Talk.query.filter_by(sender=uid).all()
        if not alls: return []
        return alls
    
    @staticmethod
    def Talksrecver(uid:int) -> list:
        alls = Talk.query.filter_by(recver=uid).all()
        if not alls: return []
        return alls
    
    @staticmethod
    def Talks(a:int, b:int) -> list:
        talks_fliter = or_(
            and_(
                Talk.sender == a,
                Talk.recver == b
            ),
            and_(
                Talk.sender == b,
                Talk.recver == a
            )
        )
        alls = Talk.query.filter(*talks_fliter).all()
        return alls
    
    # commit

    @staticmethod
    def Send(sender:int, recver:int, context) -> bool:
        if Extension.Has(sender) and Extension.Has(recver):
            msg = Talk(sender=sender, recver=recver, context=context)

            shown_list = Show.query.filter_by(hoster=recver, shown=sender).first()
            if shown_list:
                shown_list.redots += 1
            else:
                shown_list = Show(hoster=recver, shown=sender)
                db.session.add(shown_list)

            db.session.add(msg)
            db.session.commit()
            
            recver = Extension.Getbyid(recver)
            if recver.current == '': return True
            data = {
                'uid':sender,
                'context':context
            }
            emit('message', data, room=recver.current)

            return True
        else:
            return False
    
    @staticmethod
    def Sidin(uid, sid):
        if not Extension.Has(uid):return
        user = Extension.Getbyid(uid)
        user.current = sid
        db.session.commit()
    
    @staticmethod
    def Sidout(uid):
        if not Extension.Has(uid):return
        user = Extension.Getbyid(uid)
        user.current = ''
        db.session.commit()


class Chat(Namespace):
    def on_connect(self, auth):
        if type(auth) != dict: return False
        current = User.query.filter_by(name = auth.get('name')).first()
        if not current: return False
        if current.pswd != auth.get('pswd'): return False
        Extension.Sidin(current.id, request.sid)
        session['crt'] = current
        print(current.name, 'connected.')

    def on_disconnect(self):
        Extension.Sidout(session['crt'].id)
        print(session['crt'].name, 'disconnected.')

    def on_person(self, data:dict):
        uid  = data.get('uid')
        text = data.get('context')
        Extension.Send(session['crt'].id, uid, text)

    def on_group(self):
        pass

    def on_list(self):
        print('req list')
        shown = Show.query.filter_by(hoster = session['crt'].id).all()
        if not shown:emit('list', ['clear', {}])
        else:
            results = {}
            for i in shown:
                frds = User.query.filter_by(id = i.shown).first()
                results[i.id] = {
                    'name':frds.name,
                    'frid':frds.id
                }
            res = ['create', results]
            print(res)
            emit('list', res)