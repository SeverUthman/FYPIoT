import os
import uuid
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
from auth.azauth import azauth
from routes.home import home
from kitchen.kitchenmanagement import kitchenmanagement
from iothub.iot import iot

import app_config


app = Flask(__name__)
app.secret_key = 'aT17Q~5F-DkJ.uhRJpeNFcbQfGNL-1x658-Nv' 
app.config.from_object(app_config)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


def create_app():
    app = Flask(__name__)   
    app.secret_key = 'aT17Q~5F-DkJ.uhRJpeNFcbQfGNL-1x658-Nv' 
    app.config.from_object(app_config)
    Session(app)
    from database import db
    # register a blueprint for authorization.
    app.register_blueprint(azauth, url_prefix="/auth")
    # register the home/index blueprint
    app.register_blueprint(home, url_prefix="")
    # register the kitchen management blueprint
    app.register_blueprint(kitchenmanagement, url_prefix="/kitchenmanagement")
    # register the IoT Hub blueprint
    app.register_blueprint(iot, url_prefix="/iot")

    db.db.init_app(app)
    return app

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Azure App
    # Service, a docker container will be used to publish the app, likely running a web server like gunicorn
    app = create_app()
    app.config.from_object(app_config)
    app.secret_key = 'aT17Q~5F-DkJ.uhRJpeNFcbQfGNL-1x658-Nv' 
    app.config.from_object(app_config)
    #Session(app)
    app.run(host='localhost', port=5000, debug=True)
else:
    app = create_app()
    app.secret_key = 'aT17Q~5F-DkJ.uhRJpeNFcbQfGNL-1x658-Nv' 

#if __name__ == "__main__":
#    app.run()

