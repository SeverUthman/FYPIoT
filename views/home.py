import traceback
import requests
import msal

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect, session
from auth.azauth import azauth

home = Blueprint("home", __name__, static_folder="../static/", template_folder="../templates/")

# The default (aka home) route for the app
@home.route('/', methods=['POST', 'GET'])
def index():
    if not session.get("user"):
        print("returning page auth/login")
        return redirect("https://kitchencontrol.azurewebsites.net/auth/login")
    return render_template('index.html', user=session["user"], version=msal.__version__)