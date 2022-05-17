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

'''
This route will create a user by submitting an HTTP Post API call to the
Azure Active Directory API.
But the AAD User API only creates the user, so after creation the route makes another
call to the Groups API, in order to the user to the appropriate group (admin or user)
'''
@admin.route("createuser",  methods=['POST', 'GET'])
def createuser():
    try:
        if request.method == 'POST':
            token = getTokenFromCache(app_config.SCOPE) # gets an OAuth2 token to authorize using AAD APIs
            if not token:
                return False
            
            response, updateresponse, userid = CreateUserAndAddEmail(token)

            # create the HTTP request to quert AAD API and get a list of groups
            groups = requests.get(
                app_config.GROUPSENDPOINT+"?$filter=startswith(displayName, 'kitchencontrol')",
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }    
            )
            # so that we don't hard code the group ID in code, look for the appropriate group in AAD and get its ID
            groupid=''
            # this will have a value and be true when tested if the user being created needs to be an admin. Otherwise it will be null.
            isadmin = request.form.get('isadmin')

            jsongroups = json.loads(groups.text)
            for jsongroup in jsongroups['value']:
                # check the groups, and pick the right group based on user type.
                groupName = jsongroup['displayName']
                if(isadmin):
                    if("Admin" in groupName):
                        groupid = jsongroup['id']
                if(not isadmin):
                    if("User" in groupName):
                        groupid = jsongroup['id']

            # now that we have the right group ID, add the new user to the appropriate group
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
            return render_template("createuser.html")
        else:
            return render_template("createuser.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

# This helper method will actually create the user in AAD based on values fillled in the web form.
def CreateUserAndAddEmail(token):
    # Get all the user details
    userprincipalname = request.form['upn']
    givenname = request.form['fname']
    surname = request.form['lname']
    displayname = request.form['fname']+" "+request.form['lname']
    email = request.form['email']
    temppw = request.form['temppw']

    # build the HTTP request to create the user
    response = requests.post(
                app_config.ENDPOINT,
                headers={
                            'Authorization': 'Bearer ' + token['access_token'],
                            'Content-type': 'application/json'
                        }, 
                # the payload for data in the body needs to be in JSON format
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

    # As the user address cannot be added to the user on creation, we have to subsequently add that after creation.
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

# This is an application end point that calls Azure AD, querying whether a user already exists with the details
# the user is attempting to submit for a new user.
@admin.route("/checkuserexists/<string:upn>",  methods=['GET'])
def checkusereixsts(upn):
    token = getTokenFromCache(app_config.SCOPE)
    if not token:
        return False
    
    # by adding the UPN to the end of the users endpoint, the AAD API will treat the request as a query and
    # if a user with that UPN exists, it'll return the user object signalling that they exist.
    # if it does not find the user, it'll return a 404 error.
    response = requests.get(
        app_config.ENDPOINT+"/"+upn,
        headers={
                    'Authorization': 'Bearer ' + token['access_token'],
                    'Content-type': 'application/json'
                }
    )

    # return the status code to the caller, 200 will indicate the user exists, 404 will indicate the user does not already exist.
    return str(response.status_code)

# This route will display gather the user details and send them to the view to render.
# Posting to this method will be to update the user type status (i/e from admin to non admin and vice versa)
@admin.route("/showuser/<int:userid>", methods=['POST', 'GET'])
def showuser(userid):
    try:
        if request.method == 'POST':
            userisadmin = request.form.get('isadmin')
            # this helper will check what the user needs to be and sets it as such
            dbhelper.UpdateUserAdmin(userid, userisadmin)
            # get the user, kitchensn and viable kitchens objects as we will need to send it back to the page to render it's details after loading again
            user = dbhelper.GetUser(userid)
            kitchens = dbhelper.GetAllKitchensForUser(userid)
            viablekitchens = dbhelper.GetAllViableKitchensForUser(kitchens)
            return render_template('showuser.html', user=user, kitchens=kitchens, viablekitchens=viablekitchens)
        else:
            user = dbhelper.GetUser(userid)
            kitchens = dbhelper.GetAllKitchensForUser(userid)
            viablekitchens = dbhelper.GetAllViableKitchensForUser(kitchens)
            return render_template('showuser.html', user=user, kitchens=kitchens, viablekitchens=viablekitchens)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

# This route will take a kitchen ID and a user ID and associate the two by creating a relationship
# in the database user_kitchens table
@admin.route("/addkitchenstouser/<string:kitchenids>/<string:userid>", methods=["POST"])
def addkitchenstouser(kitchenids, userid):
    returnlist = []
    try:
        for kitchenid in kitchenids.split(","):
            print(kitchenid)
            kitchen = dbhelper.GetKitchen(kitchenid)
            dbhelper.AssociateUserToKitchen(kitchen, userid)
            # This method is primarily called by jquery ajax which will need to update the view
            # based on the new list of associated kitchens. To follow MVC architecture, we should not
            # manipulate the data on the view, and if we send back only the list of associated kitchens then the list
            # on the view will not be ordered. Therefore we send back a complete (and ordered) list of kitchens associated
            # with the user which jQuery can rebuild on screen.
            returnlist.append([kitchen.nickname, kitchen.kitchen_id])
        return json.dumps(returnlist), 200, {'ContentType':'application/json'}
    except Exception as e:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 

# This route will take a kitchen ID and a user ID and remove the association of the two by removing a relationship
# in the database user_kitchens table
@admin.route("/removekitchensfromuser/<string:kitchenids>/<string:userid>", methods=["POST"])
def removekitchensfromuser(kitchenids, userid):
    returnlist = []
    try:
        user = dbhelper.GetUser(userid)
        for kitchenid in kitchenids.split(","):
            print(kitchenid)
            kitchen = dbhelper.GetKitchen(kitchenid)
            dbhelper.RemoveKitchenFromUser(kitchen, user)
            # This method is primarily called by jquery ajax which will need to update the view
            # based on the new list of associated kitchens. To follow MVC architecture, we should not
            # manipulate the data on the view, and if we send back only the list of associated kitchens then the list
            # on the view will not be ordered. Therefore we send back a complete (and ordered) list of kitchens associated
            # with the user which jQuery can rebuild on screen.
            returnlist.append([kitchen.nickname, kitchen.kitchen_id])
        return json.dumps(returnlist), 200, {'ContentType':'application/json'}
    except Exception as e:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 

# This route returns a list of all users to the view for an administrator to manage.
@admin.route("/allusers", methods=["GET"])
def allusers():
    try:
        userstoreturn = dbhelper.GetAllUsers()
        return render_template("allusers.html", users=userstoreturn)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

# This route will take a user ID, get the record from the application database.
# Then it will call the Azure AAD API to disable a user and pass the Azure ID of the user found on the application database.
# Then it will update the application database to show the user is disbabled, and
# Finally the view redirects the user to the user's page.
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

# This route will take a user ID, get the record from the application database.
# Then it will call the Azure AAD API to enable a user and pass the Azure ID of the user found on the application database.
# Then it will update the application database to show the user is enabled, and
# Finally the view redirects the user to the user's page.
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


# This route will create a "strong password" against the azure app registration
# and returns the Azure generated credential.
# Microsoft recommends never to store this key and only the recipient having accesses,
# therefore we don't store the key and instruct the user in the view to save the key as
# it is impossible to retrieve in the future
@admin.route("/createapi", methods=['POST', 'GET'])
def createapi():
    try:
        if request.method == 'POST':
            token = getTokenFromCache(app_config.SCOPE)
            if not token:
                return False
            else:
                # use the customer name to build a unique name for the key that can be used to identify API call sources.
                customername = request.form.get('name')
                response = requests.post(
                            "https://graph.microsoft.com/v1.0/applications/bbe83e6c-7848-4c73-89ee-600b17e9750d/addPassword",
                            headers={
                                        'Authorization': 'Bearer ' + token['access_token'],
                                        'Content-type': 'application/json'
                                    }, 
                            data = json.dumps({
                                        "passwordCredential": {
                                            "displayName": customername+"_CreatedAPIKeyFromCode",
                                            "endDateTime": "2119-05-01T10:18:33.4995826Z", # for this project, a very long expiry time has been created, but this can be shortened or even parameterised in the form
                                            "startDateTime": "2019-05-01T10:18:33.4995826Z"
                                        }
                                    })
                        )
            results = json.loads(response.text)
            return render_template("createapi.html", keydetails=results)
        else:
            return render_template("createapi.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)