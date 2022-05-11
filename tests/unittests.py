from mock import patch
patch('auth.azauth.login_required', lambda x: x).start()

from flask import session, url_for
from database import dbhelper
from app import create_app


app = create_app()
app.app_context().push()
from database.db import db

with app.test_client() as test_client:
    with test_client.session_transaction() as mock_session:
        mock_session["user"] = "1"



def test_getuserfromdb():
    assert dbhelper.GetUser(1).first_name == 'Test1'


def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        print(response.data)
        assert b"Take control of your Kitchen" in response.data