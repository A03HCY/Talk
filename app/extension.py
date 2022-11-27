from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request

import os

db  = SQLAlchemy()
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/info')
def root():
    data = {
        'services':{
            'talknet':'/talk'
        },
    }
    return jsonify(data)

@api.route('avatar')
def avatar():
    uid = request.args.get('uid', 'er')
    return uid

