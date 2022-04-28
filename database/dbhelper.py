from flask_sqlalchemy import SQLAlchemy
from flask import app, Flask
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import relationship
#from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from database import db

'''
Gets all the registerd IoT devices with joins to associated objects
so we can show useful additional information to the user about the IoT device on a summary page
'''
def GetAllIoTDevices():
    # This query uses outer joins because we want to be able to show any devices that have not been associated to a kitchen or appliance
    query = db.db.session.query(\
                        db.iot_device.iot_device_id.label('iotid'),\
                        db.iot_device.nickname.label('iotname'),\
                        db.iot_device.kitchen_appliance_type_id.label('iotkitchenappid'),\
                        db.kitchen_appliance_type.kitchen_appliance_type.label('kitchenappliancetype'),\
                        db.kitchen_appliance.nickname.label('kitchenappliance'),\
                        db.kitchen.nickname.label('kitchen'),\
                        db.kitchen.kitchen_id.label('kitchenid'))\
                        .select_from(db.iot_device)\
                        .join(db.kitchen_appliance)\
                        .join(db.kitchen_appliance_type)\
                        .join(db.kitchen)
    devices = query.all()
    return devices

'''
Returns a kitchen appliance object and sends the appliance ID as a secondary variable
for ease of use
'''
def GetKitchenApplianceAndTypeID(applianceid):
    kitchenappliance = db.db.session.query(db.kitchen_appliance).filter_by(kitchen_appliance_id = applianceid).first()
    appliancetypeid = kitchenappliance.kitchen_appliance_type_id
    return kitchenappliance,appliancetypeid

'''
Add an IoT device to the database 
This should be called after a user creates a Digital Twin using the IoT Hub
and we can store the details of the twin in our database for ease of use
'''
def RegisterIoTDeviceInDB(kitchenappliance, appliancetypeid, devicename, newdevice, connstring):
    iotdevice = db.iot_device(device_etag=newdevice.etag, nickname=devicename, connstring=connstring, kitchen_appliance_type_id=appliancetypeid)
    db.db.session.add(iotdevice)
    db.db.session.commit()

    kitchenappliance.iot_device_id = iotdevice.iot_device_id
    db.db.session.commit()

'''
Get all kitchens for a user
'''
def GetAllKitchens(user_id):
    kitchens = db.db.session.query(db.kitchen)\
                                    .join(db.user_kitchen)\
                                    .filter(db.user_kitchen.user_id == user_id)\
                                    .all()
                            
    return kitchens

'''
Get the details of an IoT Device
'''
def GetIoTDeviceDetails(deviceid):
    devicedetails = db.iot_device.query\
                        .join(db.kitchen_appliance, db.iot_device.iot_device_id == db.kitchen_appliance.iot_device_id)\
                        .join(db.kitchen_appliance_type, db.iot_device.kitchen_appliance_type_id == db.kitchen_appliance_type.kitchen_appliance_type_id)\
                        .join(db.kitchen, db.kitchen_appliance.kitchen_id == db.kitchen.kitchen_id)\
                        .join(db.user_kitchen, db.kitchen.kitchen_id == db.user_kitchen.kitchen_id)\
                        .with_entities(
                            db.iot_device.iot_device_id.label('iotid'),\
                            db.iot_device.nickname.label('iotname'),\
                            db.iot_device.pollfrequency.label('iotpollfrequency'),\
                            db.iot_device.alertthreshold.label('iotalertthreshold'),\
                            db.iot_device.kitchen_appliance_type_id.label('iotkitchenappid'),\
                            db.kitchen_appliance.nickname.label('kitchenappliance'),\
                            db.kitchen_appliance.kitchen_appliance_id.label('applianceid'),\
                            db.kitchen_appliance_type.kitchen_appliance_type.label('appliancetype'),\
                            db.kitchen.nickname.label('kitchen'),\
                            db.kitchen.kitchen_id.label('kitchenid')\
                        )\
                        .where(db.iot_device.iot_device_id == deviceid)\
                        .first()
                    
    return devicedetails


'''
Get the Top15 latest telemetry details for a specificed IoT Device
We need the appliance type because oven and fridge temperatures are stored in the same table
so this helps us differentiate between what is needed. Scale history is in it's own table
'''
def GetTop15DeviceTelemetry(deviceid, appliancetype):
    if appliancetype == "Oven":
        telemetry = db.db.session.query(db.oven_temp_history)\
                                    .filter(db.oven_temp_history.iot_device_id == deviceid)\
                                    .order_by(desc(db.oven_temp_history.reading_datetime))\
                                    .limit(15)\
                                    .all()
    elif appliancetype == "Fridge":
        telemetry = db.db.session.query(db.fridge_temp_history)\
                                    .filter(db.fridge_temp_history.iot_device_id == deviceid)\
                                    .order_by(desc(db.fridge_temp_history.reading_datetime))\
                                    .limit(15)\
                                    .all()
    elif appliancetype == "Scale":
        telemetry = db.db.session.query(db.scale_history)\
                                    .filter(db.scale_history.iot_device_id == deviceid)\
                                    .order_by(desc(db.scale_history.reading_datetime))\
                                    .limit(15)\
                                    .all()
    else:
        # do not hide errors, bubble them up to the calling method so they can be hanlded appropriately
        return Exception
    
    dicttelemetry = []
    for result in telemetry:
        if appliancetype == "Oven" or "Fridge":
            telpoint = [result.reading_datetime.strftime("%m/%d/%Y, %H:%M:%S"), str(result.tempC), str(result.tempF)]
            dicttelemetry.append(telpoint)
        elif appliancetype == "Scale":
            telpoint = [result.reading_datetime.strftime("%m/%d/%Y, %H:%M:%S"), str(result.weight)]
            dicttelemetry.append(telpoint)
    return dicttelemetry


'''
Change the poll time frequency setting on the database for an IoT Device
'''
def ChangeDevicePollTime(deviceid, newpolltime):
    device = db.db.session.query(db.iot_device).filter(db.iot_device.iot_device_id == deviceid).first()
    device.pollfrequency = newpolltime
    db.db.session.commit()
    return device

'''
Change the threshold setting on the database for the device before it raises an alert
'''
def ChangeDeviceAlertThreshold(deviceid, newthreshold):
    device = db.db.session.query(db.iot_device).filter(db.iot_device.iot_device_id == deviceid).first()
    device.alertthreshold = newthreshold
    db.db.session.commit()
    return device

'''
Returns list of appliances that have been registered for a particular kitchen
'''
def GetAppliancesForKitchen(kitchid):
    kitchenappliances = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid).all()
    return kitchenappliances

'''
Create a new kitchen entry in the database
'''
def CreateNewKitchen(name, firstline, secondline, city, postcode, country):
    new_kitchen = db.kitchen(nickname=name, line1=firstline, line2=secondline, city=city, postcode=postcode, country=country)      
    db.db.session.add(new_kitchen)
    db.db.session.commit()
    return new_kitchen

'''
Adds the relationship between user and kitchen in the user_kitchens table
'''
def AssociateUserToKitchen(new_kitchen, userid):
    currentuser = db.user.query.filter_by(user_id=userid).first()
    currentuser.kitchens.append(new_kitchen)
    return currentuser

'''
A user should only have one default kitchen associated to them.
This method sets the default kitchen value. If it's true, it'll look for any existing kitchens
which are set as the default, update their value so they are no longer the default kitchen and 
finally set the passed kitchen identity as the default for the passed user
'''
def SetDefaultKitchenStatusForUser(isdefaultkitchen, kitchen, user):
    if isdefaultkitchen:
        olddefaultkitchen = db.db.session.query(db.user_kitchen).filter( 
                    db.user_kitchen.user_id == user.user_id,
                    db.user_kitchen.is_default_kitchen == True).first()
        if olddefaultkitchen:
            olddefaultkitchen.is_default_kitchen = False

        userkitchens = db.db.session.query(db.user_kitchen).filter(
                    db.user_kitchen.kitchen_id == kitchen.kitchen_id, 
                    db.user_kitchen.user_id == user.user_id).first()
        userkitchens.is_default_kitchen = True
    else:
        userkitchens = db.db.session.query(db.user_kitchen).filter(
                    db.user_kitchen.kitchen_id == kitchen.kitchen_id, 
                    db.user_kitchen.user_id == user.user_id).first()
        userkitchens.is_default_kitchen = False
    db.db.session.commit()

'''
Get Kitchen from ID
'''
def GetKitchen(kitchid):
    return db.kitchen.query.filter_by(kitchen_id=kitchid).first()

'''
Fetch the User
'''
def GetUser(userid):
    return db.user.query.filter_by(user_id=userid).first()

'''
Fetch User_Kitchen object
'''
def GetUser_KitchenObject(kid, uid):
    return db.db.session.query(db.user_kitchen).filter(
                db.user_kitchen.kitchen_id == kid, 
                db.user_kitchen.user_id == uid).first()

def GetScalesForKitchen(kitchid):
    return db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=3).all()

def GetFridgesForKitchen(kitchid):
    return db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=2).all()

def GetOvensForKitchen(kitchid):
    return db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=1).all()

def GetAllKitchensForUser(userid):
    return db.db.session.query(db.kitchen).filter(db.user_kitchen.user_id == userid).all()

def GetCountOfApplianceInKitchen(kitchen, appliancetypeid):
    return db.db.session.query(db.kitchen_appliance).filter(db.kitchen_appliance.kitchen_id == kitchen.kitchen_id, db.kitchen_appliance.kitchen_appliance_type_id == appliancetypeid).count()

def GetKitchenApplianceByID(applianceid):
    return db.kitchen_appliance.query.filter_by(kitchen_appliance_id=applianceid).first()

def CreateNewAppliance(name, selectedkitchen, appliancetypeid):
    new_appliance = db.kitchen_appliance(nickname=name, kitchen_id=selectedkitchen, kitchen_appliance_type_id=appliancetypeid)
    db.db.session.add(new_appliance)
    db.db.session.commit()

def GetUserByAzureID(uoid):
    return db.user.query.filter_by(user_az_id=uoid).first()

def CreateNewUserInDatabase(uoid, fname, lname, email, isadmin):
    return db.user(user_az_id=uoid, first_name=fname, last_name=lname, email=email, is_admin=isadmin)