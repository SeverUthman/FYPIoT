import os
import uuid
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from auth.azauth import azauth
from views.home import home

import app_config


app = Flask(__name__)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


def create_app():
    app = Flask(__name__)
    #app.config.from_object("config.DevConfig")
    
    # register a blueprint for authorization.
    app.register_blueprint(azauth, url_prefix="/auth")
    app.register_blueprint(home, url_prefix="")
    
    return app

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Azure App
    # Service, a webserver process such as Gunicorn will serve the app.
    app = create_app()
    app.config.from_object(app_config)
    Session(app)
    app.run(host='localhost', port=5000, debug=True)
else:
    app = create_app()
# [END gae_python3_app]
# [END gae_python38_app]


app.jinja_env.globals.update(_build_auth_code_flow=azauth._build_auth_code_flow)  # Used in template

#if __name__ == "__main__":
#    app.run()

