# Microsoft provides a python library for authentication called MSAL (Microsoft Authentication Library) upon which the code below was built
# Documentation for the MSAl can be found here: https://msal-python.readthedocs.io/en/latest/?badge=latest
import json
from pickle import TRUE

import app_config
import msal
import requests
import objectpath
from functools import wraps
from flask import jsonify, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from database import dbhelper

# Register this file as a Blueprint to be used in the application
azauth = Blueprint("azauth", __name__, static_folder="../static/", template_folder="../templates/")

@azauth.route("/login")
def login():
    # Go through the login process with the helper methods in this class.
    # Pass the scopes (i/e the types of information about the user we want) as part of the auth process
    # so we can get the information we need in the session, such as group membership to distinguish admin and standard users.
    # The user will need to approve / consent to the request the first time they access and authenticate against the application
    # to sharing the data we ask for
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    authurl=session["flow"]["auth_uri"]

    if("localhost" not in authurl):
        authurl = authurl.replace("redirect_uri=http%", "redirect_uri=https%")
    return render_template("login.html", auth_url=authurl, version=msal.__version__)


# Once a user has been prompted for credentials and authenticate successfully against Azure AD
# Azure App Registration will contact the the application on this route to pass the credential token
# that has just been created
@azauth.route(app_config.REDIRECT_PATH)  # setting the route value using a config file allows us to change the route in one config location only
def authorized():
    try:
        print("In MSAL try statement")
        # the application uses a single cache for the whole instance, so we want to load it
        cache = loadSessionCache()
        # get an instance of the confidential client application and call the acquire token by auth code flow method to retieve an
        # authorisation code. 
        result = buildAzureMSALApp(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("login_failure.html", result=result) # cleanly redirect to an error page if we hit a problem with the authentication
        session["user"] = result.get("id_token_claims") # store the user token details in the session cache so it can be picked up later if needed
        uoid = result.get("id_token_claims").get("oid")
        session["user_az_id"] = uoid # store the user object id in a separate session cookie for ease of use
        session.modified = True
        saveAppCache(cache) # update the msal cache 

        # check if this is a new user or a returning user
        currentuserindb = dbhelper.GetUserByAzureID(uoid)
        try:
            if not currentuserindb: # if this is a new user
                basicdetails = getUserBasicDetails() # get their basic details to create a DB record for them
                fname = basicdetails[0]
                lname = basicdetails[1]
                email = '' if basicdetails[2] is None else basicdetails[2]
                isadmin = checkUserIsAdmin() # check if they are part of the administrator group in active directory to automatically assign them administrator roles
                isenabled = True
                newuser = dbhelper.CreateNewUserInDatabase(uoid, fname, lname, email, isadmin) # create a new user database record
                session["user_id"] = newuser.user_id # store the user database ID in the session for ease of querying (saves us having to look up user by Azure ID then getting DB ID)
                session["is_admin"] = isadmin
            else:
                session["user_id"] = currentuserindb.user_id
                session["is_admin"] = currentuserindb.is_admin
        except Exception as e:
            return render_template("errorpage.html", errorstack=e) # reroute the error page if something goes wrong with DB interaction

    except ValueError:  # not sure why but sometimes an error happens, believe it's a bug with the MSAL library
        pass  # we can ignore this error and let the code run
    return redirect(url_for("home.index")) # once user has been authenticated, redirect the browser to the home page




# This method removes the user credentials from the session to effectively "log out" the user
@azauth.route("/logout")
def logout():
    session.clear()  # Remove all credentials from the session (user and token cache)
    return redirect(  # The redirect will go to the Azure App Registration application's logout URL to terminate the session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("home.index", _external=True)) # and once it has logged out / terminated the App Registration session, the user will be redirected to the Home.Index view

# This method is used to get more information about the user from Azure Active Directory using Microsoft Graph API
@azauth.route("/graphcall")
def graphcall():
    token = getTokenFromCache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)

# This method will look to the server-side token cache for the sessions (this is configured in the app_config.py)
# and if it can find it (i/e we have created a session previously and stored credentials in the session cache)
# then return the results, deseialize so the code can use it and return the object
# otherwise it returns null
def loadSessionCache():
    sessionCache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        sessionCache.deserialize(session["token_cache"])
    return sessionCache

# this method checks for a flag that shows the token cachce has changed
# if it has, then update the session cache with the updated token cache
def saveAppCache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

# This method creates an instance of a Confidential client application that represents
# the Azure App Registration application and will be used to manage credentials and tokens
def buildAzureMSALApp(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY, client_credential=app_config.CLIENT_SECRET, token_cache=cache)

# This method will first get the confidential client application for this web app
# then it will initiate the authentication flow and passing along any scopes (i/e details we want to get about the user from Azure Active Directory)
# and where to send the web browser once authentication has completed.
def _build_auth_code_flow(authority=None, scopes=None):
    # there is a bug in the MSAL code provided by Microsoft which does not offer the redirect_uri for the login to HTTPS (instead it gives HTTP)
    # this causes problems with Azure App Registration because 1. We must use SSL as basic security requirement and 2. Even if we don't want to use SSL, App Registration does not let us register an HTTP redirect URI.
    # This code checks if we are in local development (therefore don't need HTTPS) or deployed on a server. If deployed on server then ensure the URI generated is SSL (i/e with an HTTPS schema) to match the Azure App Registration redirect URI
    # effectively forcing any HTTP URI to be replaced with HTTPS
    if("localhost" in url_for("azauth.authorized", _external=True)):
        urlfor = url_for("azauth.authorized", _external=True)
    else:
        urlfor = url_for("azauth.authorized", _external=True, _scheme='https')
        
    return buildAzureMSALApp(authority=authority).initiate_auth_code_flow(
        scopes or [], # scopes an optional parameter, so check if something has been passed along and use it. If nothing passed, don't request any specific scopes.
        redirect_uri=urlfor) # set the authorized view as the redirect url when authentication completes.

# if user is already logged in and we have stored a token in the session
# then we can use this method to find the token in the session to save us
# time in going back to azure and getting another token
def getTokenFromCache(scope=None):
    cache = loadSessionCache()  # This web app maintains one cache per session
    confidentialClientApplication = buildAzureMSALApp(cache=cache) # get the logical representation of the Azure App Registration that does our authentication and credential management
    accounts = confidentialClientApplication.get_accounts() # get a list of accounts that have previously signed in and have been stored in cache (https://docs.microsoft.com/en-us/python/api/msal/msal.application.clientapplication?view=azure-python#msal-application-clientapplication-get-accounts)
    if accounts:
        result = confidentialClientApplication.acquire_token_silent(scope, account=accounts[0]) # get any existing tokens for the user account that are in the msal cache
        saveAppCache(cache) # save any updates for the user tokens to the cache
        return result

# Custom authentication decorator that can be used to check if the logged in user has already logged in and authenticated successfully
# by checking the session["user"] server session cookie which is set when a user is logged in and cleared when a user logs out.
# If the user is not logged in, then they cannot see the website and will be rerouted to the login page.
def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            # ensure the user has already authenticated by checking for tokens in the user session cookie
            if not session["user"]:
                # if user is not authenticated, redirect to the login page
                return redirect(url_for("azauth.login"))
            # Otherwise the user is authenticated and can proceed
            return f(*args, **kwargs)
        except Exception as e:
            # if a problem occurs during the check for authentication, assume the user is not authenticated and route to log in page.
            return redirect(url_for("azauth.login"))
    return decorator

# Custom authorization decorator that can be used to limit access to functionality on the website to administrators only.
# It works by checking for a value on the session["isadmin"] server cookie which is set when an administrator user
# logs in, and is cleared when a user logs out.
def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            # ensure the user is an administrator
            if not session["isadmin"]:
                # if user is not an administrator
                return redirect(url_for("azauth.needadminperm"))
            # Otherwise the user is an administrator and can proceed
            return f(*args, **kwargs)
        except Exception as e:
            # if a problem occurs during the check for admin, assume the user is not an admin and route need permissions page.
            return redirect(url_for("azauth.needadminperm"))
    return decorator


def getUserBasicDetails():
    # this is the token created when the user logs in, needed to authenticate against the Microsoft Graph API
    token = getTokenFromCache(app_config.SCOPE)
    if not token:
        return redirect(url_for("azauth.login"))
    # use HTTP GET call on the Microsoft Graph API with an Endpoint (URL) for the group membership
    basicdetails = requests.get( 
        app_config.USERENDPOINT, # the endpoint URL for User details on Graph API
        headers={'Authorization': 'Bearer ' + token['access_token']}, # Need to pass the bearer token for authentication
        ).json() # format the returned results as JSON
    
    firstname = basicdetails.get('givenName')
    lastname = basicdetails.get('surname')
    email = basicdetails.get('mail')

    return firstname,lastname,email


# This method will check if the user logging in is an administrator
# if they are an administrator, then add a session cookie so the custom decorator
# can check against the cookie and allow the user through to any view or functions that need elevated permissions
def checkUserIsAdmin():
    userisadmin = False
    # this is the token created when the user logs in, needed to authenticate against the Microsoft Graph API
    token = getTokenFromCache(app_config.SCOPE)
    # if there is no token, then presume the user has not logged in and therefore redirect to login page
    if not token:
        return redirect(url_for("azauth.login"))
    # use HTTP GET call on the Microsoft Graph API with an Endpoint (URL) for the group membership
    groupMembership = requests.get( 
        app_config.MEMBEROFENDPOINT, # the endpoint URL for Group Membership on Graph API
        headers={'Authorization': 'Bearer ' + token['access_token']}, # Need to pass the bearer token for authentication
        ).json() # format the returned results as JSON
    
    # The returned results will be a list of groups and details of the groups from Azure Active Directory in JSON format
    # Use the ObjectPath library to search against the returned results
    treeObject = objectpath.Tree(groupMembership)
    result = tuple(treeObject.execute("$.value[@.displayName is '"+app_config.KITCHENCONTROLADMINGROUPNAME+"']"))

    # if we find the user is a member of the admin group
    if result:
        session["isadmin"] = True # set the session cookie for isadmin to true
        userisadmin = True
    for entry in result: # development / debug code
        print(entry)

    return userisadmin

