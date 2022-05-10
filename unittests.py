from flask import url_for
from database import dbhelper
from app import create_app

app = create_app()
app.app_context().push()
from database.db import db

def test_getuserfromdb():
    assert dbhelper.GetUser(1).first_name == 'Test1'

def test_getKitchenRoute():
    assert app.route('http://localhost:5000/kitchenmanagement/showkitchen/1') == 'stuff'