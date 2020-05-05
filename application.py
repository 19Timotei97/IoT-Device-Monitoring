import wiotp.sdk.application
from gateway_client import get_gateway_cilent


# Credențiale folosite pentru IBM Cloudant
CLOUDANT_CREDS = {
  "apikey": "AG4Y2YGsjGVRlHgcPdFjoAqSUBKr5SBevjfdS6yLSza4",
  "host": "06ef9091-300d-403a-9c18-9e496fa09e25-bluemix.cloudantnosqldb.appdomain.cloud",
  "password": "4fee4d79fd6666422bad2fbb4ccdecb42b6aee42ae72c0548331e36f14bddee7",
  "port": 443,
  "username": "06ef9091-300d-403a-9c18-9e496fa09e25-bluemix"
}

# Legarea serviciilor
SERVICE_BINDING = {
    "name": "Timotei_IoT_DM",
    "description": "Test Cloudant Binding",
    "type": "cloudant",
    "credentials": CLOUDANT_CREDS
}

ANDROID_DEVICE_TYPE = "OnePlus7Pro"
GATEWAY_DEVICE_TYPE = "LegionY520"
STATUS_EVENT_TYPE = "status"


def get_application_client(config_file_path):
    config = wiotp.sdk.application.parseConfigFile(config_file_path)
    app_client = wiotp.sdk.application.ApplicationClient(config)
    return app_client


def create_cloudant_connections(client, service_binding):
    # Legarea aplicației la IBM Cloudant (din păcate, această funcționalitate încă nu merge corect)
    cloudant_service = client.serviceBindings.create(service_binding)

    # Crearea conetorului
    connector = client.dsc.create(
        name="connector_1", type="cloudant", serviceId=cloudant_service.id, timezone="UTC",
        description="Data connector", enabled=True
    )

    # Crearea unei destinațiie sub conectorul creat
    destination_1 = connector.destinations.create(name="sensor-data", bucketInterval="DAY")

    # Crearea unei reguli de rutare a statusurilor evenimentelor Android către destinația creată
    connector.rules.createEventRule(
        name="status_events", destinationName=destination_1.name, typeId=ANDROID_DEVICE_TYPE, eventId=STATUS_EVENT_TYPE,
        description="Send android status events", enabled=True
    )

    # Crearea unei alte destinații sub același conector
    destination_2 = connector.destinations.create(name="gateway-data", bucketInterval="DAY")

    # Crearea unei reguli asemănătoare cu cea de mai sus
    connector.rules.createEventRule(
        name="status_events", destinationName=destination_2.name, typeId=GATEWAY_DEVICE_TYPE, eventId=STATUS_EVENT_TYPE,
        description="Gateway status events", enabled=True)


# Funcție de trimitere a comenzii de reset
def send_reset_command(client, type, id):
    data = {'reset': True}
    client.publishCommand(type, id, "reset", "json", data)


app_client = get_gateway_cilent("app_config.yml")
app_client.connect()


create_cloudant_connections(app_client, SERVICE_BINDING)
