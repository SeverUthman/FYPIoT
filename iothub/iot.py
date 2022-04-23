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
        query = db.db.session.query(\
                                db.iot_device.iot_device_id.label('iotid'),\
                                db.iot_device.nickname.label('iotname'),\
                                db.iot_device.kitchen_appliance_type_id.label('iotkitchenappid'),\
                                db.kitchen_appliance_type.kitchen_appliance_type.label('kitchenappliancetype'),\
                                db.kitchen_appliance.nickname.label('kitchenappliance'),\
                                db.kitchen.nickname.label('kitchen'))\
                                .select_from(db.iot_device)\
                                .outerjoin(db.kitchen_appliance_type)\
                                .outerjoin(db.kitchen_appliance)\
                                .outerjoin(db.kitchen)
        devices = query.all()
        return render_template('alldevices.html', devices = devices)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

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
            kitchens = db.db.session.query(db.kitchen).all()
            appliancetypes = db.db.session.query(db.kitchen_appliance_type).all()
            return render_template("createiotdevice.html", kitchens=kitchens, appliancetypes=appliancetypes)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@iot.route("/applianceforkitchen/<string:kitchid>")
def applianceforkitchen(kitchid):
    kitchenappliances = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid).all()
    dictappliances = []
    for appliance in kitchenappliances:
        dictresult = {'id': str(appliance.kitchen_appliance_id), 'name': appliance.nickname}
        dictappliances.append(dictresult)
    return jsonify(dictappliances)


@iot.route("/hub", methods=['GET'])
def hub():
    try:
        return render_template("createormanageiotdevices.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)