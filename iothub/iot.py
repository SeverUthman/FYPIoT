from decimal import Decimal
from flask import Flask, jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from sqlalchemy import desc
from database import db
import app_config
from iothub import iothubhelper
from database import dbhelper

# Register this file as a Blueprint to be used in the application
iot = Blueprint("iot", __name__, static_folder="../static/", template_folder="../templates/")

'''
Displays a list of all the IoT Device Digital Twins (i/e all devices registered on IoT Hub to create an identity for a physical sensor)
'''
@iot.route("/alldevices", methods=['GET'])
def alldevices():
    try:
        devices = dbhelper.GetAllIoTDevices()
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
            kitchenappliance, appliancetypeid = dbhelper.GetKitchenApplianceAndTypeID(applianceid)

            devicename = (request.form['namept1']+request.form['namept2']+request.form['namept3']).replace(" ", "")
            newdevice, primarykey = iothubhelper.createIoTDevice(devicename)
            connstring = 'HostName={hostname};DeviceId={devicename};SharedAccessKey={accesskey}'.format(hostname=app_config.IOTHUBHOSTNAME, devicename=devicename, accesskey=primarykey)

            dbhelper.RegisterIoTDeviceInDB(kitchenappliance, appliancetypeid, devicename, newdevice, connstring)
            return "Your device is created, your shared access key is {connectionstring}".format(connectionstring=connstring)
        else:
            kitchens = dbhelper.GetAllKitchens(session['user_id'])
            return render_template("createiotdevice.html", kitchens=kitchens)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


'''
This route will return the requested IoT device
'''
@iot.route("/showdevice/<int:deviceid>", methods=['GET'])
def showdevice(deviceid):
    try:
        devicedetails = dbhelper.GetIoTDeviceDetails(deviceid)
        telemetry = dbhelper.GetTop15DeviceTelemetry(deviceid, devicedetails.appliancetype)
        #device = db.iot_device.query().filter_by(iot_device_id=deviceid).first()
        return render_template("showiotdevice.html", device=devicedetails, telemetry=telemetry)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)



@iot.route("/gettemptelemetry/<int:deviceid>", methods=['GET'])
def gettemptelemetry(deviceid):
    try:
        dicttelemetry = dbhelper.GetTop15DeviceTelemetry(deviceid, "Oven")
        return jsonify(dicttelemetry)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@iot.route("/updatedevicepolltime/<int:deviceid>", methods=['POST'])
def updatedevicepolltime(deviceid):
    try:
        newpolltime =  request.form['newpolltime']
        device = dbhelper.ChangeDevicePollTime(deviceid, newpolltime)
        iothubhelper.updatePollTimeOnDevice(newpolltime, device.nickname)
        return redirect(url_for('iot.showdevice', deviceid=deviceid))
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)



@iot.route("/updatedevicethreshold/<int:deviceid>", methods=['POST'])
def updatedevicethreshold(deviceid):
    try:
        newthreshold =  request.form['newthreshold']
        device = dbhelper.ChangeDeviceAlertThreshold(deviceid, newthreshold)
        iothubhelper.updateAlertThresholdOnDevice(newthreshold, device.nickname)
        return redirect(url_for('iot.showdevice', deviceid=deviceid))
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)



'''
This route will primarily be called from an ajax javascript call
when the user is creating an IoT device, to get the list of appliances
for the user's selected Kitchen which enables the registered IoT device to be
associated with the correct appliance on creation.
'''
@iot.route("/applianceforkitchen/<string:kitchid>")
def applianceforkitchen(kitchid):
    kitchenappliances = dbhelper.GetAppliancesForKitchen(kitchid)
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