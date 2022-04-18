from flask_sqlalchemy import SQLAlchemy
from flask import app, Flask
from datetime import datetime
#from flask_sqlalchemy_session import flask_scoped_session

db = SQLAlchemy()

def IsUserRegistered():
    return False

user_kitchen = db.Table('user_kitchen',
            db.Column('user_kitchen_id', db.Integer, primary_key=True),
            db.Column('is_default_kitchen', db.Boolean),
            db.Column('kitchen_id', db.Integer, db.ForeignKey('kitchen.kitchen_id')),
            db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
)

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __repr__(self):
        return '<user %r>' % self.user_id

class kitchen(db.Model):
    kitchen_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    line1 = db.Column(db.String(50))
    line2 = db.Column(db.String(50))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(50))
    country = db.Column(db.String(50))

    def __repr__(self):
        return '<kitchen %r>' % self.kitchen_id

class kitchen_appliance_type(db.Model):
    kitchen_appliance_type_id = db.Column(db.Integer, primary_key=True)
    kitchen_appliance_type = db.Column(db.String(100))

    def __repr__(self):
        return '<kitchen_appliance_type %r>' % self.kitchen_appliance_type_id

class iot_device(db.Model):
    iot_device_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    kitchen_appliance_type_id = db.Column('kitchen_appliance_type_id', db.Integer, db.ForeignKey('kitchen_appliance_type.kitchen_appliance_type_id'))

    def __repr__(self):
        return '<iot_device %r>' % self.iot_device_id

class kitchen_appliance(db.Model):
    kitchen_appliance_id = db.Column(db.Integer, primary_key=True)
    kitchen_appliance_type_id = db.Column('kitchen_appliance_type_id', db.Integer, db.ForeignKey('kitchen_appliance_type.kitchen_appliance_type_id'))
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))

    def __repr__(self):
        return '<kitchen_appliance %r>' % self.kitchen_appliance_id

class oven_temp_history(db.Model):
    oven_temp_history_id = db.Column(db.Integer, primary_key=True)
    tempC = db.Column(db.Numeric(5,2))
    tempF = db.Column(db.Numeric(5,2))
    reading_datetime = db.Column(db.TIMESTAMP)
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))

    def __repr__(self):
        return '<oven_temp_history %r>' % self.oven_temp_history_id

class fridge_temp_history(db.Model):
    fridge_temp_history_id = db.Column(db.Integer, primary_key=True)
    tempC = db.Column(db.Numeric(5,2))
    tempF = db.Column(db.Numeric(5,2))
    reading_datetime = db.Column(db.TIMESTAMP)
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))

    def __repr__(self):
        return '<fridge_temp_history %r>' % self.fridge_temp_history_id

class scale_history(db.Model):
    scale_history_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(5,2))
    reading_datetime = db.Column(db.TIMESTAMP)
    iot_device_id = db.Column('iot_device_id', db.Integer, db.ForeignKey('iot_device.iot_device_id'))

    def __repr__(self):
        return '<scale_history %r>' % self.scale_history_id


