import app_config, string, random
from azure.iot.hub import IoTHubRegistryManager, DigitalTwinClient
from azure.iot.hub.models import QuerySpecification

'''
This method will use the IoT Hub SDK to get a list of IoT devices registered on the hub
'''
def getAllIOTDevices():
    hub = IoTHubRegistryManager.from_connection_string(app_config.IOTHUBCONN)
    query = QuerySpecification(query='SELECT * FROM devices')

    results = hub.query_iot_hub(query,None,None)
    return results

'''
This method will use the IoT Hub SDK to create a new IoT Digital Twin
'''
def createIoTDevice(device_id, status='enabled', iot_edge=False, status_reason='Just created', device_scope=None, parent_scopes=None):
    ltrs = string.ascii_letters # define this to create random strings
    primary_key = ''.join(random.choice(ltrs) for i in range(24)) # create a strong 24 character random string for access keys
    secondary_key = ''.join(random.choice(ltrs) for i in range(24))
    hub = IoTHubRegistryManager.from_connection_string(app_config.IOTHUBCONN) # instantiate an IoT hub instance
    # create a new device in the IoT Hub
    newdevice = hub.create_device_with_sas(device_id=device_id, primary_key=primary_key, secondary_key=secondary_key, status=status, iot_edge=iot_edge, status_reason=status_reason, device_scope=device_scope, parent_scopes=parent_scopes)
    return newdevice, primary_key # return the pertinet detail to the requestor 

'''
This method will send a direct message to the IoT device.
It will use the device name to find the device to contact
then send a message
'''
def updatePollTimeOnDevice(newpolltime, devicename):
    try:
        twinclient = DigitalTwinClient.from_connection_string(app_config.IOTHUBCONN)
        # the message, i/e "ChangeReadFrequency", must match exactly the message the IoT device is expecting to receive
        result = twinclient.invoke_command(
            devicename, "ChangeReadFrequency", newpolltime, 3, 7
        )

        if result:
            return True
        else:
            return False
    except Exception as e:
        return e

'''
This method will send a direct message to the IoT device.
It will use the device name to find the device to contact
then send a message to update the alert threshold
'''
def updateAlertThresholdOnDevice(newthreshold, devicename):
    try:
        twinclient = DigitalTwinClient.from_connection_string(app_config.IOTHUBCONN)
        # the action value must match the value on the iot device, exactly.
        result = twinclient.invoke_command(
            devicename, "ChangeAlertThreshold", newthreshold, 3, 7
        )

        if result:
            return True
        else:
            return False
    except Exception as e:
        return e