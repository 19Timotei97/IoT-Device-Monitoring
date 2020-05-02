import wiotp.sdk.application


# Credențiale folosite pentru IBM Cloudant
CLOUDANT_CREDS = {
  "apikey": "your_api_key_here",
  "host": "eeca8e52-1774-4698-93d1-cafa434762ac-bluemix.cloudantnosqldb.appdomain.cloud",
  "password": "your_pwd_here",
  "port": 443,
  "username": "your_username_here"
}

# Legarea serviciilor
SERVICE_BINDING = {
    "name": "any-binding-name",
    "description": "Test Cloudant Binding",
    "type": "cloudant",
    "credentials": CLOUDANT_CREDS
}

ANDROID_DEVICE_TYPE = "Android"
GATEWAY_DEVICE_TYPE = "raspi"
STATUS_EVENT_TYPE = "status"


def get_application_client(config_file_path):
    config = wiotp.sdk.application.parseConfigFile(config_file_path)
    app_client = wiotp.sdk.application.ApplicationClient(config)
    return app_client


def create_cloudant_connections(client, service_binding):
    # Legarea aplicației la IBM Cloudant (din păcate, a suferit schimbări majore)
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

