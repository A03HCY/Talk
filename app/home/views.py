from . import home_blue
from flask import render_template

@home_blue.route('/')
def welcome():
    return render_template('login.html')