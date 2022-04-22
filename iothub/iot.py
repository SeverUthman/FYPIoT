from flask import Flask, jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from database import db
import app_config
from iothub import iothubhelper

# Register this file as a Blueprint to be used in the application
iot = Blueprint("iot", __name__, static_folder="../static/", template_folder="../templates/")


@iot.route("/alldevices", methods=['POST', 'GET'])
def alldevices():
    try:
        if request.method == 'POST':
            pass
        else:
            devices = iothubhelper.getAllIOTDevices()
            for device in devices.items:
                print(device)
            return jsonify(devices.items)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@iot.route("/createdevice", methods=['POST', 'GET'])
def createdevice():
    try:
        if request.method == 'POST':
            pass
            devicename = request.form['namept1']+request.form['namept2']+request.form['namept3']
            appliancetypeid = request.form['appliancetypeid']
            newdevice, primarykey = iothubhelper.createIoTDevice(devicename)
            connstring = 'HostName={hostname};DeviceId={devicename};SharedAccessKey={accesskey}'.format(hostname=app_config.IOTHUBHOSTNAME, devicename=devicename, accesskey=primarykey)

            iotdevice = db.iot_device(device_etag=newdevice.etag, nickname=devicename, connstring=connstring, kitchen_appliance_type_id=appliancetypeid)
            db.db.session.add(iotdevice)
            db.db.session.commit()
            return "Your device is created, your shared access key is {connectionstring}".format(connectionstring=connstring)
        else:
            kitchens = db.db.session.query(db.kitchen).all()
            appliancetypes = db.db.session.query(db.kitchen_appliance_type).all()
            return render_template("createiotdevice.html", kitchens=kitchens, appliancetypes=appliancetypes)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@iot.route("/hub", methods=['GET'])
def hub():
    try:
        return render_template("createormanageiotdevices.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)