from flask_sqlalchemy import SQLAlchemy
from flask import app, Flask
from datetime import datetime
from sqlalchemy.orm import relationship
#from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

"""
from app import create_app
app = create_app()
app.app_context().push()
from database.db import db
#db.create_all()
#db.drop_all()
#db.create_all()

"""

db = SQLAlchemy()

def IsUserRegistered():
    return False

""" user_kitchen = db.Table('user_kitchen',
            db.Column('user_kitchen_id', db.Integer, primary_key=True),
            db.Column('is_default_kitchen', db.Boolean),
            db.Column('kitchen_id', db.Integer, db.ForeignKey('kitchen.kitchen_id')),
            db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
) """

class kitchen(db.Model):
    __tablename__ = "kitchen"
    kitchen_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    line1 = db.Column(db.String(50))
    line2 = db.Column(db.String(50))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(50))
    country = db.Column(db.String(50))

    users = relationship("user", secondary="user_kitchen")
    
    def __repr__(self):
        return '<kitchen %r>' % self.kitchen_id
        

class user(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_az_id = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    kitchens = relationship("kitchen", secondary="user_kitchen", lazy='dynamic')

    def __repr__(self):
        return '<user %r>' % self.user_id


class user_kitchen(db.Model):
    __tablename__ = "user_kitchen"
    kitchen_id = db.Column(db.ForeignKey('kitchen.kitchen_id'), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), primary_key=True)
    is_default_kitchen = db.Column('is_default_kitchen', db.Boolean)

    kitchen = relationship("kitchen", backref="user_associations")
    user = relationship("user", backref="kitchen_associations")


class kitchen_appliance_type(db.Model):
    kitchen_appliance_type_id = db.Column(db.Integer, primary_key=True)
    kitchen_appliance_type = db.Column(db.String(100))

    def __repr__(self):
        return '<kitchen_appliance_type %r>' % self.kitchen_appliance_type_id


class iot_device(db.Model):
    iot_device_id = db.Column(db.Integer, primary_key=True)
    device_etag = db.Column(db.String(12))
    nickname = db.Column(db.String(100))
    connstring = db.Column(db.String(256))
    kitchen_appliance_type_id = db.Column('kitchen_appliance_type_id', db.Integer, db.ForeignKey('kitchen_appliance_type.kitchen_appliance_type_id'))
    pollfrequency = db.Column(db.Integer)
    alertthreshold = db.Column(db.Numeric(5,2))

    def __repr__(self):
        return '<iot_device %r>' % self.iot_device_id

class kitchen_appliance(db.Model):
    kitchen_appliance_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    kitchen_id = db.Column('kitchen_id', db.Integer, db.ForeignKey('kitchen.kitchen_id'))
    kitchen_appliance_type_id = db.Column('kitchen_appliance_type_id', db.Integer, db.ForeignKey('kitchen_appliance_type.kitchen_appliance_type_id'))
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))

    def __repr__(self):
        return '<kitchen_appliance %r>' % self.kitchen_appliance_id

class oven_temp_history(db.Model):
    oven_temp_history_id = db.Column(db.Integer, primary_key=True)
    reading_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))
    tempC = db.Column(db.Numeric(5,2))
    tempF = db.Column(db.Numeric(5,2)) 

    def __repr__(self):
        return '<oven_temp_history %r>' % self.oven_temp_history_id

class fridge_temp_history(db.Model):
    fridge_temp_history_id = db.Column(db.Integer, primary_key=True)
    reading_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))
    tempC = db.Column(db.Numeric(5,2))
    tempF = db.Column(db.Numeric(5,2))
    
    def __repr__(self):
        return '<fridge_temp_history %r>' % self.fridge_temp_history_id

class scale_history(db.Model):
    scale_history_id = db.Column(db.Integer, primary_key=True)
    reading_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))
    weight = db.Column(db.Numeric(5,2))

    def __repr__(self):
        return '<scale_history %r>' % self.scale_history_id


