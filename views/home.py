import traceback
import requests
import msal

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
from database import db

home = Blueprint("home", __name__, static_folder="../static/", template_folder="../templates/")

# The default (aka home) route for the app
@home.route('/', methods=['POST', 'GET'])
def index():
    
    if not session.get("user"):

        try:    
            #return redirect("http://localhost:5000/auth/login")
            return redirect(url_for("azauth.login"))
        except Exception as e:
            return traceback.print_tb(e.__traceback__, limit=None, file=None)
    fname = "Sever" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    newuser = db.user(first_name=fname, last_name="Miranbeg, ", email="sev123miranbeg@gmail.com")
    db.db.session.add(newuser)
    db.db.session.commit()

    users = db.user.query.all()
    print("**-*-*-**--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* "+str(users))
    for user in users:
        print("found user: " + str(user.user_id) + " " + user.first_name + " " + user.last_name)
    return render_template('index.html', user=session["user"], version=msal.__version__)