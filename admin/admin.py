from decimal import Decimal
import json
from flask import jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
import requests
from sqlalchemy import desc
from auth.azauth import getTokenFromCache
from database import db
import app_config
from iothub import iothubhelper
from database import dbhelper

# Register this file as a Blueprint to be used in the application
admin = Blueprint("admin", __name__, static_folder="../static/", template_folder="../templates/")

@admin.route("createuser",  methods=['POST', 'GET'])
def createuser():
    try:
        if request.method == 'POST':
            token = getTokenFromCache(app_config.SCOPE)
            if not token:
                return False
            
            response, updateresponse, userid = CreateUserAndAddEmail(token)

            groups = requests.get(
                app_config.GROUPSENDPOINT+"?$filter=startswith(displayName, 'kitchencontrol')",
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }    
            )
            groupid=''
            isadmin = request.form.get('isadmin')

            jsongroups = json.loads(groups.text)
            for jsongroup in jsongroups['value']:
                groupName = jsongroup['displayName']
                if(isadmin):
                    if("Admin" in groupName):
                        groupid = jsongroup['id']
                if(not isadmin):
                    if("User" in groupName):
                        groupid = jsongroup['id']

            addtogroup = requests.post(
                app_config.GROUPSENDPOINT+"/"+groupid+"/members/$ref",
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        },
                data = json.dumps({
                    "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+userid
                })
                
            )
            return response, updateresponse, addtogroup
        else:
            return render_template("createuser.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

def CreateUserAndAddEmail(token):
    userprincipalname = request.form['upn']
    givenname = request.form['fname']
    surname = request.form['lname']
    displayname = request.form['fname']+" "+request.form['lname']
    email = request.form['email']
    temppw = request.form['temppw']

    response = requests.post(
                app_config.ENDPOINT,
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }, 
                data = json.dumps({
                            "accountEnabled": True,
                            "displayName": displayname,
                            "mailNickname": "Created",
                            "userPrincipalName": userprincipalname,
                            "givenname":givenname,
                            "surname":surname,
                            "passwordProfile" : 
                            {
                                "forceChangePasswordNextSignIn": True,
                                "password": temppw
                            }
                        })
            )

    id = json.loads(response.text)['id']
    updateresponse = requests.patch(
                app_config.ENDPOINT+"/"+id,
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }, 
                data = json.dumps(
                    {
                        "mail" : email
                    }
                )
            )
    
    return response,updateresponse,id

@admin.route("/checkuserexists/<string:upn>",  methods=['GET'])
def checkusereixsts(upn):
    token = getTokenFromCache(app_config.SCOPE)
    if not token:
        return False
    
    response = requests.get(
        app_config.ENDPOINT+"/"+upn,
        headers={
                    'Authorization': 'Bearer ' + token['access_token'],
                    'Content-type': 'application/json'
                }
    )

    return str(response.status_code)

@admin.route("/showuser/<int:userid>", methods=['GET'])
def showuser(userid):
    try:
        if request.method == 'POST':
            return render_template('showuser.html')
        else:
            user = dbhelper.GetUser(userid)
            kitchens = dbhelper.GetAllKitchensForUser(userid)
            viablekitchens = dbhelper.GetAllViableKitchensForUser(kitchens)
            return render_template('showuser.html', user=user, kitchens=kitchens, viablekitchens=viablekitchens)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@admin.route("/addkitchenstouser/<string:kitchenids>/<string:userid>", methods=["POST"])
def addkitchenstouser(kitchenids, userid):
    returnlist = []
    try:
        for kitchenid in kitchenids.split(","):
            print(kitchenid)
            kitchen = dbhelper.GetKitchen(kitchenid)
            dbhelper.AssociateUserToKitchen(kitchen, userid)
            returnlist.append([kitchen.nickname, kitchen.kitchen_id])
        return json.dumps(returnlist), 200, {'ContentType':'application/json'}
    except Exception as e:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 

@admin.route("/removekitchensfromuser/<string:kitchenids>/<string:userid>", methods=["POST"])
def removekitchensfromuser(kitchenids, userid):
    returnlist = []
    try:
        user = dbhelper.GetUser(userid)
        for kitchenid in kitchenids.split(","):
            print(kitchenid)
            kitchen = dbhelper.GetKitchen(kitchenid)
            dbhelper.RemoveKitchenFromUser(kitchen, user)
            returnlist.append([kitchen.nickname, kitchen.kitchen_id])
        return json.dumps(returnlist), 200, {'ContentType':'application/json'}
    except Exception as e:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 

@admin.route("/allusers", methods=["GET"])
def allusers():
    try:
        userstoreturn = dbhelper.GetAllUsers()
        return render_template("allusers.html", users=userstoreturn)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@admin.route("/disableuser/<string:userid>", methods=['POST'])
def disableuser(userid):
    dbhelper.DisableUser(userid)
    user = dbhelper.GetUser(userid)
    token = getTokenFromCache(app_config.SCOPE)
    if not token:
        return False
    else:
        updateresponse = requests.patch(
                app_config.ENDPOINT+"/"+user.user_az_id,
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }, 
                data = json.dumps(
                    {
                        "accountEnabled": False
                    }
                )
            )

    return redirect(url_for('admin.allusers'))

@admin.route("/enableuser/<string:userid>", methods=['POST'])
def enableuser(userid):
    dbhelper.EnableUser(userid)
    user = dbhelper.GetUser(userid)
    token = getTokenFromCache(app_config.SCOPE)
    if not token:
        return False
    else:
        updateresponse = requests.patch(
                app_config.ENDPOINT+"/"+user.user_az_id,
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }, 
                data = json.dumps(
                    {
                        "accountEnabled": True
                    }
                )
            )
    return redirect(url_for('admin.allusers'))