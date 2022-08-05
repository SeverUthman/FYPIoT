import os

CLIENT_ID = "a7bdf031-d1b4-49fa-b06c-a2f82a2cd1ac" # Application (client) ID of the App Registration in Azure Active Directory

CLIENT_SECRET = 'removing from public repo' # This client secret was generated when creating the App Registration in Azure Active Directory. It cannot be found again via Azure Portal and would need to generate a new one if it's lost.

AUTHORITY = "https://login.microsoftonline.com/4c57b01d-709a-46da-bb58-e79a9a2f3335"  # The Tenant ID of the App Registration in Azure Active Directory

REDIRECT_PATH = "/getmsaltoken" # Used for forming an absolute URL to your redirect URI.
                                # The absolute URL must match the redirect URI you set
                                # in the app's registration in the Azure portal.

# https://docs.microsoft.com/en-us/graph/permissions-reference
# The permissions to be requested / accepted by user when they first log in to the application
# to delegate control and allow this web application to read the data as if it were the user
SCOPE = ["User.ReadBasic.All", "Directory.ReadWrite.All", "Application.ReadWrite.All"]

# Microsoft Graph API has different Endpoints that can be called to get details about the user from Azure Active Directory
MEMBEROFENDPOINT = 'https://graph.microsoft.com/v1.0/me/memberof'  # Retrieves the groups the user is a part of
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # Retrieves all users in Active Directory
GROUPSENDPOINT = 'https://graph.microsoft.com/v1.0/groups'  # Retrieves all users in Active Directory
USERENDPOINT = 'https://graph.microsoft.com/v1.0/me/' # Retrieves information about the current user in Active Directory
APPLICATIONENDPOINT = 'https://graph.microsoft.com/beta/applications' # To be used with the Beta AddPassword endpoint for creating client secret API Keys
CREATEUSERENDPOINT = ''
SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://username:password@azuresqlinstance.database.windows.net/databasename?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = False

KITCHENCONTROLADMINGROUPNAME = "KitchenControlAdmin"

IOTHUBHOSTNAME = 'iothubname.azure-devices.net'
IOTHUBCONN = 'HostName=KitchenControlHub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=GENERATETHISFROMAZURE'

OVEN_APPLIANCE_TYPE_ID = 1
FRIDGE_APPLIANCE_TYPE_ID = 2
SCALE_APPLIANCE_TYPE_ID = 3
