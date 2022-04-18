from flask_sqlalchemy import SQLAlchemy
from flask import app, Flask
from datetime import datetime
#from flask_sqlalchemy_session import flask_scoped_session

db = SQLAlchemy()

def IsUserRegistered():
    return False

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __repr__(self):
        return '<user %r>' % self.user_id