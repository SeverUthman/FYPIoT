import app_config
import msal
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint

azauth = Blueprint("azauth", __name__, static_folder="../static/", template_folder="../templates/")


@azauth.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)


# Once a user has been prompted for credentials and authenticate successfully against Azure AD
# Azure App Registration will contact the the application on this route to pass the credential token
# that has just been created
@azauth.route(app_config.REDIRECT_PATH)  # setting the route value using a config file allows us to change the route in one config location only
def authorized():
    try:
        # the application uses a single cache for the whole instance, so we want to load it
        cache = loadSessionCache()
        # get an instance of the confidential client application and call the acquire token by auth code flow method to retieve an
        # authorisation code. 
        result = buildAzureMSALApp(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result) # cleanly redirect to an error page if we hit a problem with the authentication
        session["user"] = result.get("id_token_claims") # store the user token details in the session cache so it can be picked up later if needed
        saveAppCache(cache) # update the msal cache 
    except ValueError:  # not sure why but sometimes an error happens
        pass  # we can ignore this error and let the code run
    return redirect(url_for("home.index")) # once user has been authenticated, redirect the browser to the home page

@azauth.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("home.index", _external=True))

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

def _build_auth_code_flow(authority=None, scopes=None):
    return buildAzureMSALApp(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("azauth.authorized", _external=True))

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
