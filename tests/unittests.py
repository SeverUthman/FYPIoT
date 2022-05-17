import random
import string
from mock import patch
patch('auth.azauth.login_required', lambda x: x).start()

from flask import session, url_for
from database import dbhelper
from app import create_app


app = create_app()
app.app_context().push()
from database.db import db

with app.test_client() as test_client:
    with test_client.session_transaction() as mock_session:
        mock_session["user"] = "1"
        mock_session["user_id"] = "1"



def test_getuserfromdb():
    assert dbhelper.GetUser(1).first_name == 'Test1'


def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Take control of your Kitchen" in response.data

def test_iothubpage():
    with app.test_client() as test_client:
        response = test_client.get('/iot/hub')
        assert response.status_code == 200
        assert b"Register a new IoT Device on the IoT Hub or manage" in response.data

def test_iotalldevices():
    with app.test_client() as test_client:
        response = test_client.get('/iot/alldevices')
        assert response.status_code == 200
        assert b"All IoT Devices" in response.data

def test_iotshowdevice():
    with app.test_client() as test_client:
        response = test_client.get('/iot/showdevice/1')
        assert response.status_code == 200
        assert b"View your device details, telemetry and send a" in response.data

def test_iotupdatedevicepolltime():
    with app.test_client() as test_client:
        response = test_client.get('/iot/showdevice/1')
        assert response.status_code == 200
        assert b"View your device details, telemetry and send a" in response.data

        postresponse = test_client.post(
            '/iot/updatedevicepolltime/1',
            data = dict(newpolltime="300"),
            follow_redirects=True
        )
        assert postresponse.status_code == 200

        reset = test_client.post(
            '/iot/updatedevicepolltime/1',
            data = dict(newpolltime="10"),
            follow_redirects=True
        )

        assert reset.status_code == 200

def test_iotupdatealertthreshold():
    with app.test_client() as test_client:
        response = test_client.get('/iot/showdevice/1')
        assert response.status_code == 200
        assert b"View your device details, telemetry and send a" in response.data

        postresponse = test_client.post(
            '/iot/updatedevicethreshold/1',
            data = dict(newthreshold="50"),
            follow_redirects=True
        )
        assert postresponse.status_code == 200

        reset = test_client.post(
            '/iot/updatedevicethreshold/1',
            data = dict(newthreshold="25"),
            follow_redirects=True
        )
        assert reset.status_code == 200

def test_iotcreatenewdeviceget():
     with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/iot/createdevice')
        assert response.status_code == 200
        assert b"If you have already registered a kitchen" in response.data

def test_iotcreatenewdevicepost():
     with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        randappend = ''
        for i in range(12):
            randappend+=(random.choice(string.ascii_letters))

        postresponse = test_client.post(
            '/iot/createdevice',
            data = dict(applianceid="1", namept1="TestKitchen1", namept2="Kitchen1Oven1", namept3="AutomatedUnitTest"+randappend),
            follow_redirects=True
        )
        assert postresponse.status_code == 200

def test_kmviewtwinsmenu():
    with app.test_client() as test_client:
        response = test_client.get('/kitchenmanagement/viewtwinsmenu')
        assert response.status_code == 200
        assert b"View your existing Digital Twins" in response.data

def test_kmgetovens():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/getovens')
        assert response.status_code == 200
        assert b"All Ovens" in response.data

def test_kmgetfridges():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/getfridges')
        assert response.status_code == 200
        assert b"All Fridges" in response.data

def test_kmgetscales():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/getscales')
        assert response.status_code == 200
        assert b"All Scales" in response.data

def test_kmregistertwinsmenu():
    with app.test_client() as test_client:
        response = test_client.get('/kitchenmanagement/registertwinsmenu')
        assert response.status_code == 200
        assert b"Register a new Kitchen or Appliances" in response.data

def test_kmregisterkitchenget():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/registerkitchen')
        assert response.status_code == 200
        assert b"Register a Kitchen" in response.data



def test_kmregisterkitchenpost():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        postresponse = test_client.post(
            '/kitchenmanagement/registerkitchen',
            data = dict(name="AutomatedUnitTestKitchen", addLine1="Automated", addLine2="Unit Test", city="PyTest", postcode="P7 T357", country="UK", defaultKitchen=False ),
            follow_redirects=True
        )
        
        assert postresponse.status_code == 200


def test_kmcreateovenget():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/createoven')
        assert response.status_code == 200
        assert b"Create an Oven Digital Twin" in response.data


def test_kmcreateovenpost():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        postresponse = test_client.post(
            '/kitchenmanagement/createoven',
            data = dict(name="AutomatedUnitTestOven", kitchenid="1"),
            follow_redirects=True
        )
        
        assert postresponse.status_code == 200

def test_kmcreatefridgeget():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/createfridge')
        assert response.status_code == 200
        assert b"Create a Fridge Digital Twin" in response.data

def test_kmcreatefridgepost():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        postresponse = test_client.post(
            '/kitchenmanagement/createfridge',
            data = dict(name="AutomatedUnitTestFridge", kitchenid="1"),
            follow_redirects=True
        )
        
        assert postresponse.status_code == 200
        
def test_kmcreatescaleget():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/kitchenmanagement/createscale')
        assert response.status_code == 200
        assert b"Create a Scale Digital Twin" in response.data

def test_kmcreatescalepost():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        postresponse = test_client.post(
            '/kitchenmanagement/createscale',
            data = dict(name="AutomatedUnitTestScale", kitchenid="1"),
            follow_redirects=True
        )
        
        assert postresponse.status_code == 200

def test_kmadminallusers():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/admin/allusers')
        assert response.status_code == 200
        assert b"All Users" in response.data

def test_kmadminshowuser():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.get('/admin/showuser/1')
        assert response.status_code == 200
        assert b"See the user details, manage their kitchens or" in response.data
        assert b"checked" in response.data

def test_kmadminshowuser_removeadminrights():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.post('/admin/showuser/2')
        assert response.status_code == 200
        assert b"See the user details, manage their kitchens or" in response.data
        assert b"checked" not in response.data

def test_kmadminshowuser_addadminrights():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.post(
            '/admin/showuser/2',
            data = dict(isadmin=True),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"See the user details, manage their kitchens or" in response.data
        assert b"checked" in response.data

def test_kmadmindisableuser():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.post(
            '/admin/disableuser/2',
            follow_redirects=True
        )
        response = test_client.get('/admin/showuser/2')
        assert response.status_code == 200
        assert b"Enable User Account" in response.data


def test_kmadminenableuser():
    with app.test_client() as test_client:
        with test_client.session_transaction() as mock_session:
            mock_session["user_id"] = 1
        response = test_client.post(
            '/admin/enableuser/2',
            follow_redirects=True
        )
        response = test_client.get('/admin/showuser/2')
        assert response.status_code == 200
        assert b"Disable User Account" in response.data
