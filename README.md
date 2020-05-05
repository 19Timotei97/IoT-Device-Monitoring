# IoT-Device-Monitoring
A simple but useful data collector and visualization tool that can send information from a client through a gateway device to IBM Watson IoT Platform, using UDP protocol.

To run the application, the following steps are required:
1. Install SensorUDP application from Google Play
2. Add the IP Address of the gateway device (e.g.: the laptop's IPv4 Address) and the Port number (6000).
3. Run main.py script using an IDE (e.g.: PyCharm was used in the example).
4. Go to https://0vj1n7.internetofthings.ibmcloud.com/dashboard/boards/a39e5d96-4589-4a9c-82bb-167747197986 to see the data sent (you should use your IBM Cloud account to create your own dashboard or go to https://dataplatform.cloud.ibm.com/dashboards/ce799329-574a-4c98-bb12-fc71f6eeb881/view/5c29e61b25ae3dd647cec8e4079825557f662059b4bb825680d77b490a642297f06817c4c82f4f5d8e135030f5eb125dc0 to see a part of the data)

This project was created based on the tutorial found at https://developer.ibm.com/tutorials/iot-lp201-build-door-monitoring-system/, created by IBM. Also, the code was used from the repository found at https://github.com/satwikkansal/ibm_iot_example.
