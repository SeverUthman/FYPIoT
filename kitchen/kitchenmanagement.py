from flask import Flask, jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from sqlalchemy import func
from auth.azauth import login_required
from database import dbhelper
import app_config

# Register this file as a Blueprint to be used in the application
kitchenmanagement = Blueprint("kitchenmanagement", __name__, static_folder="../static/", template_folder="../templates/")


'''
this route will read the form submission if it is posted to and create new kitchen digital twin
or render a page showing the form to fill in to registered a digital twin kitchen
'''
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


'''
This method will show a kitchen if it is requested via a Get method.
If it is posted to, it will be because of a form submission which only has the "default" option available
so the poster is looking to toggle the default kitchen setting.
This route returns a set of dynamic data to the view to enable dynamic building of web content, i/e data driven application
'''
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
            # prepare holders for each type of appliance telemetry
            oventelemetry = []
            fridgetelemetry = []
            scaletelemetry = []

            # Get the kitchen object and it's appliances
            kitchen = dbhelper.GetKitchen(kitchid)
            kitchenovens = dbhelper.GetOvensForKitchen(kitchid)
            kitchenfridges = dbhelper.GetFridgesForKitchen(kitchid)
            kitchenscales = dbhelper.GetScalesForKitchen(kitchid)
            user = dbhelper.GetUser(session['user_id'])

            # look for telemetry in each type of appliance, and if it's found then add it to the list to send back to the view.
            for oven in kitchenovens:
                telemetry = dbhelper.GetTop15DeviceTelemetry(oven.iot_device_id, "Oven")
                if len(telemetry) > 0:
                    oventelemetry.append(telemetry)

            for fridge in kitchenfridges:
                telemetry = dbhelper.GetTop15DeviceTelemetry(fridge.iot_device_id, "Fridge")
                if len(telemetry) > 0:
                    fridgetelemetry.append(telemetry)

            for scale in kitchenscales:
                telemetry = dbhelper.GetTop15DeviceTelemetry(scale.iot_device_id, "Scale")
                if len(telemetry) > 0:
                    scaletelemetry.append(telemetry)

            kid=kitchen.kitchen_id
            uid=user.user_id
            
            # this is needed so the view can determine whether or not to tick the box for default kitchen for user.
            userkitchen = dbhelper.GetUser_KitchenObject(kid, uid)

            if not kitchen:
                return redirect('/')
            isdefaultkitchen = userkitchen.is_default_kitchen
            return render_template("showkitchen.html", kitchen=kitchen, isdefaultkitchen=isdefaultkitchen, ovens=kitchenovens, fridges=kitchenfridges, scales=kitchenscales, oventelemetry=oventelemetry, fridgetelemetry=fridgetelemetry, scaletelemetry=scaletelemetry)#, kitchenuser=kitchenuser)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


'''
This route returns a list of all kitchens and a count of each type of appliance per kitchen
'''
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

'''
This route creates an oven digital twin representation, i/e just a record in the database
'''
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

'''
This route returns an oven digital twin representation, i/e just a record from the database
'''
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

'''
This route creates a fridge digital twin representation, i/e just a record in the database
'''
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


'''
This route returns a fridge digital twin representation, i/e just a record from the database
'''
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

'''
This route creates a scale digital twin representation, i/e just a record in the database
'''
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

'''
This route returns a scale digital twin representation, i/e just a record from the database
'''
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

'''
This route simply renders an html page for the landing page of registering digital twins menu
'''
@kitchenmanagement.route('/registertwinsmenu', methods=['GET'])
@login_required
def registertwinsmenu():
    return render_template('registerkitchenandappliance.html')

'''
This route simply renders an html page showing links to different reports for digital twin items
'''
@kitchenmanagement.route('/viewtwinsmenu', methods=['GET'])
@login_required
def viewtwinsmenu():
    return render_template('viewdigitaltwinmenu.html')

'''
This route returns all ovens associated with the logged in user
'''
@kitchenmanagement.route('/getovens', methods=['GET'])
def getovens():
    try:
        kitchenovens = dbhelper.GetAllOvensForUser(session['user_id'])
        return render_template('allovens.html', ovens=kitchenovens)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

'''
This route returns all fridges associated with the logged in user
'''
@kitchenmanagement.route('/getfridges', methods=['GET'])
def getfridges():
    try:
        kitchenfridges = dbhelper.GetAllFridgesForUser(session['user_id'])
        return render_template('allfridges.html', fridges=kitchenfridges)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

'''
This route returns all scales associated with the logged in user
'''
@kitchenmanagement.route('/getscales', methods=['GET'])
def getscales():
    try:
        kitchenscales = dbhelper.GetAllScalesForUser(session['user_id'])
        return render_template('allscales.html', scales=kitchenscales)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)