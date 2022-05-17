import traceback
import requests
import msal

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
from auth.azauth import admin_required, login_required
from auth import azauth
from database import db

home = Blueprint("home", __name__, static_folder="../static/", template_folder="../templates/")

'''
The default (aka home) route for the app
'''
@home.route('/', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')

'''
This route is a returns a staic response page informing the user of how they can get support
'''
@home.route('/support', methods=['GET'])
def support():
    return render_template('support.html')

'''
This route is a placeholer for future developments and returns a staic response page
'''
@home.route('/footer', methods=['GET'])
def footer():
    return render_template('footer.html')
