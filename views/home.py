import traceback
import requests
import msal

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect, session, url_for
from auth.azauth import azauth

home = Blueprint("home", __name__, static_folder="../static/", template_folder="../templates/")

# The default (aka home) route for the app
@home.route('/', methods=['POST', 'GET'])
def index():
    print("################################################################################################################################# returning page auth/login ---- IS IT NONE?? \n" + str(session.get("user")))
    if not session.get("user"):
        print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH returning page auth/login ---- HERE IS STUFF " + str(session.get("user")))
        #return redirect("http://localhost:5000/auth/login")
        return redirect(url_for("azauth.login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)