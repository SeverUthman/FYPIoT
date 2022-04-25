from decimal import Decimal
from flask import Flask, jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from sqlalchemy import desc
from database import db
import app_config
from iothub import iothubhelper

# Register this file as a Blueprint to be used in the application
iot = Blueprint("iot", __name__, static_folder="../static/", template_folder="../templates/")

'''
Displays a list of all the IoT Device Digital Twins (i/e all devices registered on IoT Hub to create an identity for a physical sensor)
'''
@iot.route("/alldevices", methods=['GET'])
def alldevices():
    try:
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
                                .outerjoin(db.kitchen_appliance_type)\
                                .outerjoin(db.kitchen_appliance)\
                                .outerjoin(db.kitchen)
        devices = query.all()
        return render_template('alldevices.html', devices = devices)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


'''
On a GET request, this method will get the kitchens for the logged in user
On a POST request, this method will take the form details of the Create IoT Device page
and call the IoT Hub API to create the device then register the details in our database.
'''
@iot.route("/createdevice", methods=['POST', 'GET'])
def createdevice():
    try:
        if request.method == 'POST':
            applianceid = request.form['applianceid']
            kitchenappliance = db.db.session.query(db.kitchen_appliance).filter_by(kitchen_appliance_id = applianceid).first()
            appliancetypeid = kitchenappliance.kitchen_appliance_type_id

            devicename = (request.form['namept1']+request.form['namept2']+request.form['namept3']).replace(" ", "")
            newdevice, primarykey = iothubhelper.createIoTDevice(devicename)
            connstring = 'HostName={hostname};DeviceId={devicename};SharedAccessKey={accesskey}'.format(hostname=app_config.IOTHUBHOSTNAME, devicename=devicename, accesskey=primarykey)

            iotdevice = db.iot_device(device_etag=newdevice.etag, nickname=devicename, connstring=connstring, kitchen_appliance_type_id=appliancetypeid)
            db.db.session.add(iotdevice)
            db.db.session.commit()

            kitchenappliance.iot_device_id = iotdevice.iot_device_id
            db.db.session.commit()
            return "Your device is created, your shared access key is {connectionstring}".format(connectionstring=connstring)
        else:
            kitchens = db.db.session.query(db.kitchen)\
                                    .join(db.user_kitchen)\
                                    .filter(db.user_kitchen.user_id == session['user_id'])\
                                    .all()
            #kitchens = db.kitchen.query().filter_by(user_id=session['user_id']).all()
            #appliancetypes = db.db.session.query(db.kitchen_appliance_type).all()
            return render_template("createiotdevice.html", kitchens=kitchens)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

'''
This route will return the requested IoT device
'''
@iot.route("/showdevice/<int:deviceid>", methods=['GET'])
def showdevice(deviceid):
    try:
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
                        .first()
        telemetry = getDeviceTelemetry(deviceid, devicedetails.appliancetype)
        #device = db.iot_device.query().filter_by(iot_device_id=deviceid).first()
        return render_template("showiotdevice.html", device=devicedetails, telemetry=telemetry)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@iot.route("/gettemptelemetry/<int:deviceid>", methods=['GET'])
def gettemptelemetry(deviceid):
    try:
        dicttelemetry = getDeviceTelemetry(deviceid, "Oven")
        return jsonify(dicttelemetry)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

def getoventelemetry(deviceid):
    try:
        dicttelemetry = getDeviceTelemetry(deviceid, "Oven")
        return dicttelemetry
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

def getfridgetelemetry(deviceid):
    try:
        dicttelemetry = getDeviceTelemetry(deviceid, "Fridge")
        return dicttelemetry
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

def getscaletelemetry(deviceid):
    try:
        dicttelemetry = getDeviceTelemetry(deviceid, "Scale")
        return dicttelemetry
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@iot.route("/updatedevicepolltime/<int:deviceid>", methods=['POST'])
def updatedevicepolltime(deviceid):
    try:
        newpolltime =  request.form['newpolltime']
        device = db.db.session.query(db.iot_device).filter(db.iot_device.iot_device_id == deviceid).first()
        device.pollfrequency = newpolltime
        db.db.session.commit()
        iothubhelper.updatePollTimeOnDevice(newpolltime, device.nickname)
        return redirect(url_for('iot.showdevice', deviceid=deviceid))
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@iot.route("/updatedevicethreshold/<int:deviceid>", methods=['POST'])
def updatedevicethreshold(deviceid):
    try:
        newthreshold =  request.form['newthreshold']
        device = db.db.session.query(db.iot_device).filter(db.iot_device.iot_device_id == deviceid).first()
        device.alertthreshold = newthreshold
        db.db.session.commit()
        iothubhelper.updateAlertThresholdOnDevice(newthreshold, device.nickname)
        return redirect(url_for('iot.showdevice', deviceid=deviceid))
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


def getDeviceTelemetry(deviceid, appliancetype):
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
This route will primarily be called from an ajax javascript call
when the user is creating an IoT device, to get the list of appliances
for the user's selected Kitchen which enables the registered IoT device to be
associated with the correct appliance on creation.
'''
@iot.route("/applianceforkitchen/<string:kitchid>")
def applianceforkitchen(kitchid):
    kitchenappliances = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid).all()
    dictappliances = []
    for appliance in kitchenappliances:
        dictresult = {'id': str(appliance.kitchen_appliance_id), 'name': appliance.nickname}
        dictappliances.append(dictresult)
    return jsonify(dictappliances)


'''
Simple method to return the IoT hub menu page
'''
@iot.route("/hub", methods=['GET'])
def hub():
    try:
        return render_template("createormanageiotdevices.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)