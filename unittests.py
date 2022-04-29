from database import dbhelper
from app import create_app

app = create_app()
app.app_context().push()
from database.db import db

def test_getuserfromdb():
    assert dbhelper.GetUser(1).first_name == 'S'