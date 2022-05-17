from faulthandler import is_enabled
from flask_sqlalchemy import SQLAlchemy
from flask import app, Flask
from datetime import datetime
from sqlalchemy import and_, desc, false, not_
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
                        .join(db.kitchen_appliance_type, db.iot_device.kitchen_appliance_type_id == db.kitchen_appliance_type.kitchen_appliance_type_id)\
                        .join(db.kitchen)\
                        .join(db.user_kitchen)\
                        .where(db.user_kitchen.user_id == 1)
    print(str(query))
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
    iotdevice = db.iot_device(device_etag=newdevice.etag, nickname=devicename, connstring=connstring, kitchen_appliance_type_id=appliancetypeid, pollfrequency=10, alertthreshold=25)
    db.db.session.add(iotdevice)
    db.db.session.commit()

    kitchenappliance.iot_device_id = iotdevice.iot_device_id
    db.db.session.commit()
    return iotdevice

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
                            db.iot_device.connstring.label('connstring'),\
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
        if appliancetype == "Oven" or appliancetype == "Fridge":
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
def AssociateUserToKitchen(kitchen, userid):
    currentuser = db.user.query.filter_by(user_id=userid).first()
    currentuser.kitchens.append(kitchen)
    db.db.session.commit()
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
'''
Get The scales for a specific kitchen
'''
def GetScalesForKitchen(kitchid):
    query = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=3)
    print(str(query))
    return query.all()

'''
Get The fridges for a specific kitchen
'''
def GetFridgesForKitchen(kitchid):
    query = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=2)
    print(str(query))
    return query.all()

'''
Get The ovens for a specific kitchen
'''
def GetOvensForKitchen(kitchid):
    query = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=1) 
    print(str(query))
    return query.all()

'''
Get all kitchens for a specific user
'''
def GetAllKitchensForUser(userid):
    query = db.db.session.query(db.kitchen).join(db.user_kitchen).filter(db.user_kitchen.user_id == userid)
    print(str(query)) 
    return query.all()

'''
Return a count of appliances for a kitchen, based on appliance type
'''
def GetCountOfApplianceInKitchen(kitchen, appliancetypeid):
    return db.db.session.query(db.kitchen_appliance).filter(db.kitchen_appliance.kitchen_id == kitchen.kitchen_id, db.kitchen_appliance.kitchen_appliance_type_id == appliancetypeid).count()

'''
Fetch a kitchen appliance by its ID
'''
def GetKitchenApplianceByID(applianceid):
    return db.kitchen_appliance.query.filter_by(kitchen_appliance_id=applianceid).first()

'''
Create a new appliance, based on the appliance type id
'''
def CreateNewAppliance(name, selectedkitchen, appliancetypeid):
    new_appliance = db.kitchen_appliance(nickname=name, kitchen_id=selectedkitchen, kitchen_appliance_type_id=appliancetypeid)
    db.db.session.add(new_appliance)
    db.db.session.commit()

'''
Find a user in the database, based on their azure ID
often used to check if a logging in user is a returning user and therfore has a profile on the system
or if they are a new user
'''
def GetUserByAzureID(uoid):
    return db.user.query.filter_by(user_az_id=uoid).first()

'''
Create a new user in the database
'''
def CreateNewUserInDatabase(uoid, fname, lname, email, isadmin, isenabled=True):
    newuser = db.user(user_az_id=uoid, first_name=fname, last_name=lname, email=email, is_admin=isadmin, is_enabled=isenabled)
    db.db.session.add(newuser) # add the new record to the database
    db.db.session.commit() # commit the database change

'''
For a specific user, get all the appliances of type oven
'''
def GetAllOvensForUser(uid):
    # using SQL alchemy, we can build a complex SQL query that will join several tables, select columns and label them.
    ovens = db.db.session.query(db.kitchen_appliance)\
                        .join(db.kitchen_appliance_type, db.kitchen_appliance.kitchen_appliance_type_id == db.kitchen_appliance_type.kitchen_appliance_type_id)\
                        .join(db.iot_device, db.kitchen_appliance.iot_device_id == db.iot_device.iot_device_id)\
                        .join(db.kitchen, db.kitchen_appliance.kitchen_id == db.kitchen.kitchen_id)\
                        .join(db.user_kitchen, db.kitchen.kitchen_id == db.user_kitchen.kitchen_id)\
                        .with_entities(
                            db.iot_device.iot_device_id.label('iotid'),\
                            db.iot_device.nickname.label('iotname'),\
                            db.kitchen_appliance.nickname.label('appliancename'),\
                            db.kitchen_appliance.kitchen_appliance_id.label('applianceid'),\
                            db.kitchen.nickname.label('kitchenname'),\
                            db.kitchen.kitchen_id.label('kitchenid')
                        )\
                        .where(
                            and_(
                                db.kitchen_appliance_type.kitchen_appliance_type == 'Oven',
                                db.user_kitchen.user_id == uid
                            )
                        ).all()
    return ovens

'''
For a specific user, get all the appliances of type fridge
'''
def GetAllFridgesForUser(uid):
    # using SQL alchemy, we can build a complex SQL query that will join several tables, select columns and label them.
    ovens = db.db.session.query(db.kitchen_appliance)\
                        .join(db.kitchen_appliance_type, db.kitchen_appliance.kitchen_appliance_type_id == db.kitchen_appliance_type.kitchen_appliance_type_id)\
                        .join(db.iot_device, db.kitchen_appliance.iot_device_id == db.iot_device.iot_device_id)\
                        .join(db.kitchen, db.kitchen_appliance.kitchen_id == db.kitchen.kitchen_id)\
                        .join(db.user_kitchen, db.kitchen.kitchen_id == db.user_kitchen.kitchen_id)\
                        .with_entities(
                            db.iot_device.iot_device_id.label('iotid'),\
                            db.iot_device.nickname.label('iotname'),\
                            db.kitchen_appliance.nickname.label('appliancename'),\
                            db.kitchen_appliance.kitchen_appliance_id.label('applianceid'),\
                            db.kitchen.nickname.label('kitchenname'),\
                            db.kitchen.kitchen_id.label('kitchenid')
                        )\
                        .where(
                            and_(
                                db.kitchen_appliance_type.kitchen_appliance_type == 'Fridge',
                                db.user_kitchen.user_id == uid
                            )
                        ).all()
    return ovens

'''
For a specific user, get all the appliances of type Scale
'''
def GetAllScalesForUser(uid):
    # using SQL alchemy, we can build a complex SQL query that will join several tables, select columns and label them.
    ovens = db.db.session.query(db.kitchen_appliance)\
                        .join(db.kitchen_appliance_type, db.kitchen_appliance.kitchen_appliance_type_id == db.kitchen_appliance_type.kitchen_appliance_type_id)\
                        .join(db.iot_device, db.kitchen_appliance.iot_device_id == db.iot_device.iot_device_id)\
                        .join(db.kitchen, db.kitchen_appliance.kitchen_id == db.kitchen.kitchen_id)\
                        .join(db.user_kitchen, db.kitchen.kitchen_id == db.user_kitchen.kitchen_id)\
                        .with_entities(
                            db.iot_device.iot_device_id.label('iotid'),\
                            db.iot_device.nickname.label('iotname'),\
                            db.kitchen_appliance.nickname.label('appliancename'),\
                            db.kitchen_appliance.kitchen_appliance_id.label('applianceid'),\
                            db.kitchen.nickname.label('kitchenname'),\
                            db.kitchen.kitchen_id.label('kitchenid')
                        )\
                        .where(
                            and_(
                                db.kitchen_appliance_type.kitchen_appliance_type == 'Scale',
                                db.user_kitchen.user_id == uid
                            )
                        )
    print(ovens)
    return ovens.all()

'''
This method returns a list of kitchens that are not associated with the user
and therefore are viable for association.
'''
def GetAllViableKitchensForUser(userkitchens):
    ukitchenids = []
    for ukitchen in userkitchens:
        ukitchenids.append(ukitchen.kitchen_id)
    
    viablekitchens = db.db.session.query(db.kitchen)\
                                    .where(
                                        not_(db.kitchen.kitchen_id.in_(ukitchenids))
                                    ).all()
    return viablekitchens

'''
Remove the association between a kitchen and a user, effectively removing permissions from a user to a kitchen.
'''
def RemoveKitchenFromUser(kitchen, user):
    user.kitchens.remove(kitchen)
    db.db.session.commit()

'''
get all users in the database
'''
def GetAllUsers():
    return db.db.session.query(db.user).all()

'''
update the database record for a user to show they are disabled
'''
def DisableUser(userid):
    user = db.db.session.query(db.user).where(db.user.user_id == userid).first()
    user.is_enabled = False
    db.db.session.commit()

'''
update the database record for a user to show they are enabled
'''
def EnableUser(userid):
    user = db.db.session.query(db.user).where(db.user.user_id == userid).first()
    user.is_enabled = True
    db.db.session.commit()

'''
update the database record for a user to toggle whether or not they are an admin user.
'''
def UpdateUserAdmin(userid, isadmin):
    user = db.db.session.query(db.user).where(db.user.user_id == userid).first()
    userisadmin = False
    if isadmin:
        userisadmin = True
    user.is_admin = userisadmin
    db.db.session.commit()