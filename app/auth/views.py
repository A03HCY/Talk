from . import auth_blue
from flask import render_template

@auth_blue.route('/in')
def sign_in():
    return render_template('sign.html')