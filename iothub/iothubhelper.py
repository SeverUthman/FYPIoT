import app_config, string, random
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import QuerySpecification


def getAllIOTDevices():
    hub = IoTHubRegistryManager.from_connection_string(app_config.IOTHUBCONN)
    query = QuerySpecification(query='SELECT * FROM devices')

    results = hub.query_iot_hub(query,None,None)
    return results

def createIoTDevice(device_id, status='enabled', iot_edge=False, status_reason='Just created', device_scope=None, parent_scopes=None):
    ltrs = string.ascii_letters
    primary_key = ''.join(random.choice(ltrs) for i in range(24))
    secondary_key = ''.join(random.choice(ltrs) for i in range(24))
    hub = IoTHubRegistryManager.from_connection_string(app_config.IOTHUBCONN)
    newdevice = hub.create_device_with_sas(device_id=device_id, primary_key=primary_key, secondary_key=secondary_key, status=status, iot_edge=iot_edge, status_reason=status_reason, device_scope=device_scope, parent_scopes=parent_scopes)
    return newdevice, primary_key