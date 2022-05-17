from collections import namedtuple
from decimal import Decimal
from typing import NamedTuple
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

            dbdevice = dbhelper.RegisterIoTDeviceInDB(kitchenappliance, appliancetypeid, devicename, newdevice, connstring)
            return redirect(url_for('iot.showdevice', deviceid=dbdevice.iot_device_id))
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


'''
this route will get the latest set of telemetry for a specific IoT Device.
This is often used by an ajax async call that polls frequently to get the latest data.
'''
@iot.route("/gettemptelemetry/<int:deviceid>", methods=['GET'])
def gettemptelemetry(deviceid):
    try:
        dicttelemetry = dbhelper.GetTop15DeviceTelemetry(deviceid, "Oven")
        return jsonify(dicttelemetry)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

'''
This is a more generic telemetry fetch method where an appliance type can be specified and it will
find the right place to return the data from.
'''
@iot.route("/getlatesttelemetry/<int:deviceid>/<string:appliancetype>", methods=['GET'])
def getlatesttelemetry(deviceid, appliancetype):
    try:
        dicttelemetry = dbhelper.GetTop15DeviceTelemetry(deviceid, appliancetype)
        return jsonify(dicttelemetry)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

'''
This route will be called to change the IoT Device polling time
It will call updates in two locations
1 - on the application database
2 - using the IoT Hub, it will message the IoT Device requesting it to update its poll time
'''
@iot.route("/updatedevicepolltime/<int:deviceid>", methods=['POST'])
def updatedevicepolltime(deviceid):
    try:
        newpolltime =  request.form['newpolltime']
        device = dbhelper.ChangeDevicePollTime(deviceid, newpolltime)
        iothubhelper.updatePollTimeOnDevice(newpolltime, device.nickname)
        return redirect(url_for('iot.showdevice', deviceid=deviceid))
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


'''
This route will be called to change the IoT Device alert threshold
It will call updates in two locations
1 - on the application database
2 - using the IoT Hub, it will message the IoT Device requesting it to update its alert threshold
'''
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


'''
This route contains complex data logic that build an intricate set of tuples
that represent all kitchens a user has, then within that all appliances per kitchen, then within that
all iot devices for those appliances and finally within that all telemetry data for those IoT devices.
Returns a sorted data set of named tuples that is ready to be traversed and have data rendered or manipulated.
'''
@iot.route("/dashboards", methods=['GET'])
def dashboards():
    try:
        # start by getting all kitchens for a user
        alluserkitchens = dbhelper.GetAllKitchensForUser(session["user_id"])
        # this will house the ultimate data set which will go back to the requestor
        dataset = []
        # as we did not create a class representation of this dataset type
        # we create named tuples to easily access the data once it is compiled
        OvenData = namedtuple('OvenData', 'ApplianceName TelemetryData')
        FridgeData = namedtuple('FridgeData', 'ApplianceName TelemetryData')
        ScaleData = namedtuple('ScaleData', 'ApplianceName TelemetryData')
        ResultDataSet = namedtuple('ResultDataSet', 'Kitchen kitchenovens kitchenfridges kitchenscales oventelemetry fridgetelemetry scaletelemetry')
        
        # for every kitchen
        for kitchen in alluserkitchens:
            kitchid = kitchen.kitchen_id

            # Create empty lists for the telemetry for each type of appliance that could be present at this kitchen
            oventelemetry = []
            fridgetelemetry = []
            scaletelemetry = []

            # get a list of appliances per appliance type.
            kitchenovens = dbhelper.GetOvensForKitchen(kitchid)
            kitchenfridges = dbhelper.GetFridgesForKitchen(kitchid)
            kitchenscales = dbhelper.GetScalesForKitchen(kitchid)
            # get the user object so we can confirm which datasets they have access to
            user = dbhelper.GetUser(session['user_id'])

            # get the telemetry for every appliance of type oven in this kitchen
            for oven in kitchenovens:
                telemetry = dbhelper.GetTop15DeviceTelemetry(oven.iot_device_id, "Oven")
                if telemetry:
                    # add the telemetry to the list
                    oventelemetry.append(OvenData(oven.nickname, telemetry))

            # get the telemetry for every appliance of type fridge in this kitchen
            for fridge in kitchenfridges:
                telemetry = dbhelper.GetTop15DeviceTelemetry(fridge.iot_device_id, "Fridge")
                if telemetry:
                    # add the telemetry to the list
                    fridgetelemetry.append(FridgeData(fridge.nickname, telemetry))
            
            # get the telemetry for every appliance of type scale in this kitchen
            for scale in kitchenscales:
                telemetry = dbhelper.GetTop15DeviceTelemetry(scale.iot_device_id, "Scale")
                if telemetry:
                    # add the telemetry to the list
                    scaletelemetry.append(ScaleData(scale.nickname, telemetry))

            kid=kitchen.kitchen_id
            uid=user.user_id

            # return a dataset made up of a set of tuples, where the first layer is a tuple of
            # kitchen and list of appliance types
            # then the second layer, for every appliance type - a tuple of appliance type and appliance telemetry
            # then the final layer, where data exists, a tuple of iot device name and 2d datase.
            dataset.append(ResultDataSet(kitchen, kitchenovens, kitchenfridges, kitchenscales, oventelemetry, fridgetelemetry, scaletelemetry))
            

        return render_template('dashboards.html', dataset=dataset)
        
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)