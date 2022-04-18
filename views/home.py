import traceback
import requests
import msal

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
from auth.azauth import admin_required, login_required
from database import db

home = Blueprint("home", __name__, static_folder="../static/", template_folder="../templates/")

# The default (aka home) route for the app
@home.route('/', methods=['POST', 'GET'])
@login_required
def index():
    # check if the user has been logged in by checking session cookie for user tokens
    # if user is not logged in, then reroute them to the login page
    #if not session.get("user"):
    #    try:
    #        return redirect(url_for("azauth.login"))
    #    except Exception as e:
    #        return traceback.print_tb(e.__traceback__, limit=None, file=None)
    return render_template('index.html', user=session["user"], version=msal.__version__)