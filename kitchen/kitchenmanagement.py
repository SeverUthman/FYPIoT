from flask import Flask, jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from sqlalchemy import func
from database import dbhelper
import app_config

# Register this file as a Blueprint to be used in the application
kitchenmanagement = Blueprint("kitchenmanagement", __name__, static_folder="../static/", template_folder="../templates/")


@kitchenmanagement.route("/registerkitchen", methods=['POST', 'GET'])
def registerkitchen():
    try:
        if request.method == 'POST':
            name = request.form['name']
            firstline = request.form['addLine1']
            secondline = request.form['addLine2']
            city = request.form['city']
            postcode = request.form['postcode']
            country = request.form['country']
            defaultkitchen = request.form.get('defaultKitchen')
            new_kitchen = dbhelper.CreateNewKitchen(name, firstline, secondline, city, postcode, country)

            userid = session["user_id"]
            currentuser = dbhelper.AssociateUserToKitchen(new_kitchen, userid)

            dbhelper.SetDefaultKitchenStatusForUser(defaultkitchen, new_kitchen, currentuser)

            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=new_kitchen.kitchen_id))
        else:
            return render_template("registerkitchen.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)



@kitchenmanagement.route("/showkitchen/<string:kitchid>", methods=['GET', 'POST'])
def showkitchen(kitchid):
    try:
        if request.method == 'POST':
            kitchen = dbhelper.GetKitchen(kitchid)
            isdefaultkitchen = request.form.get('defaultKitchen')   
            user = dbhelper.GetUser(session['user_id'])
            userkitchen = dbhelper.SetDefaultKitchenStatusForUser(isdefaultkitchen, kitchen, user)
            return redirect('/kitchenmanagement/showkitchen/'+kitchid)
        else:
            oventelemetry = []
            fridgetelemetry = []
            scaletelemetry = []

            kitchen = dbhelper.GetKitchen(kitchid)
            kitchenovens = dbhelper.GetOvensForKitchen(kitchid)
            kitchenfridges = dbhelper.GetFridgesForKitchen(kitchid)
            kitchenscales = dbhelper.GetScalesForKitchen(kitchid)
            user = dbhelper.GetUser(session['user_id'])

            for oven in kitchenovens:
                telemetry = dbhelper.GetTop15DeviceTelemetry(oven.iot_device_id, "Oven")
                if len(telemetry) > 0:
                    oventelemetry.append(telemetry)

            for fridge in kitchenfridges:
                telemetry = dbhelper.GetTop15DeviceTelemetry(oven.iot_device_id, "Fridge")
                if len(telemetry) > 0:
                    fridgetelemetry.append(telemetry)

            for scale in kitchenscales:
                telemetry = dbhelper.GetTop15DeviceTelemetry(oven.iot_device_id, "Scale")
                if len(telemetry) > 0:
                    scaletelemetry.append(telemetry)

            kid=kitchen.kitchen_id
            uid=user.user_id
            
            userkitchen = dbhelper.GetUser_KitchenObject(kid, uid)

            if not kitchen:
                return redirect('/')
            isdefaultkitchen = userkitchen.is_default_kitchen
            return render_template("showkitchen.html", kitchen=kitchen, isdefaultkitchen=isdefaultkitchen, ovens=kitchenovens, fridges=kitchenfridges, scales=kitchenscales, oventelemetry=oventelemetry, fridgetelemetry=fridgetelemetry, scaletelemetry=scaletelemetry)#, kitchenuser=kitchenuser)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)



@kitchenmanagement.route("/allkitchens", methods=['GET'])
def allkitchens():
    try:
        results = []
        userkitchens = dbhelper.GetAllKitchensForUser(session['user_id'])
        for kitchen in userkitchens:
            ovens = dbhelper.GetCountOfApplianceInKitchen(kitchen, app_config.OVEN_APPLIANCE_TYPE_ID)
            fridges = dbhelper.GetCountOfApplianceInKitchen(kitchen, app_config.FRIDGE_APPLIANCE_TYPE_ID)
            scales = dbhelper.GetCountOfApplianceInKitchen(kitchen, app_config.SCALE_APPLIANCE_TYPE_ID)
            results.append([kitchen, ovens, fridges, scales])

        return render_template("allkitchens.html", kitchens=results)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/createoven", methods=['POST', 'GET'])
def createoven():
    try:
        if request.method == 'POST':
            name = request.form['name']
            selectedkitchen = request.form.get('kitchenid')
            dbhelper.CreateNewAppliance(name, selectedkitchen, app_config.OVEN_APPLIANCE_TYPE_ID)
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=selectedkitchen))
        else:
            kitchens = dbhelper.GetAllKitchensForUser(session['user_id'])
            return render_template("createoven.html", kitchens=kitchens)

    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/showoven/<int:ovenid>", methods=['POST', 'GET'])
def showoven(ovenid):
    try:
        if request.method == 'POST':
            pass
        else:
            oven = dbhelper.GetKitchenApplianceByID(ovenid)
            kitchen = dbhelper.GetKitchen(oven.kitchen_id)
            
            return render_template("showoven.html", ovendetails=oven, kitchendetails=kitchen)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/createfridge", methods=['POST', 'GET'])
def createfridge():
    try:
        if request.method == 'POST':
            name = request.form['name']
            selectedkitchen = request.form.get('kitchenid')
            dbhelper.CreateNewAppliance(name, selectedkitchen, app_config.FRIDGE_APPLIANCE_TYPE_ID)
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=selectedkitchen))
        else:
            kitchens = dbhelper.GetAllKitchensForUser(session['user_id'])
            return render_template("createfridge.html", kitchens=kitchens)

    except Exception as e:
        return render_template("errorpage.html", errorstack=e)



@kitchenmanagement.route("/showfridge/<int:fridgeid>", methods=['POST', 'GET'])
def showfridge(fridgeid):
    try:
        if request.method == 'POST':
            pass
        else:
            fridge = dbhelper.GetKitchenApplianceByID(fridgeid)
            kitchen = dbhelper.GetKitchen(fridge.kitchen_id)
            return render_template("showfridge.html", fridgedetails=fridge, kitchendetails=kitchen)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/createscale", methods=['POST', 'GET'])
def createscale():
    try:
        if request.method == 'POST':
            name = request.form['name']
            selectedkitchen = request.form.get('kitchenid')
            dbhelper.CreateNewAppliance(name, selectedkitchen, app_config.SCALE_APPLIANCE_TYPE_ID)
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=selectedkitchen))
        else:
            kitchens = dbhelper.GetAllKitchensForUser(session['user_id'])
            return render_template("createscale.html", kitchens=kitchens)

    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/showscale/<int:scaleid>", methods=['POST', 'GET'])
def showscale(scaleid):
    try:
        if request.method == 'POST':
            pass
        else:
            scale = dbhelper.GetKitchenApplianceByID(scaleid)
            kitchen = dbhelper.GetKitchen(scale.kitchen_id)
            return render_template("showscale.html", scaledetails=scale, kitchendetails=kitchen)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)