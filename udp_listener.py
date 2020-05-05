# Fișier ce conține parsarea de date prin UDP prin socket-uri

import socket
from struct import unpack_from
import csv
from datetime import datetime

UDP_IP = "0.0.0.0" # Adresa IP pentru UDP
UDP_PORT = 6000 # Portul pe care sunt transmise informațiile

# Proprietățile care pot fi vizualizate prin aplicația de pe device
properties = ['x_acc', 'y_acc', 'z_acc', 'x_gravity', 'y_gravity', 'z_gravity',  'x_rotation', 'y_rotation',
              'z_rotation', 'x_orientation', 'y_orientation', 'z_orientation', 'deprecated_1', 'deprecated_2',
              'ambient_light', 'proximity', 'keyboard_button_pressed']


# Funcție folosită pentru a extrage datele din structura folosită
def unpack_and_return(data, offset):
    return unpack_from("!f", data, offset)[0]


# Funcție ce este utilizată pentru a gestiona datele primite
# Am modificat această funcție pentru a trimite datele primite de la senzori
# Într-un fișier csv, pentru o analiză ulterioară
def process_data(data):
    offset = 0
    result = {}
    sensors = ["timestamp"]

    # Extrage toate proprietățile disponibile din aplicația SensorUDP
    for property in properties:
        sensors.append(property)

    # Scrie toate coloanele în fișierul .csv
    with open('IoTData.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(sensors)

    for property in properties:
        result[property] = unpack_and_return(data, offset)
        offset += 4
    return result


# Funcție folosită pentru a asculta pe portul potrivit datele trimise
def listen_sensor_data():
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM) # Protocolul UDP
    sock.bind((UDP_IP, UDP_PORT))
    values = []

    while True:
        data, addr = sock.recvfrom(1024) # Dimensiunea buffer-ului este de 1024 octeți
        data = process_data(data)

        # Pentru depanarea programului, printează toate datele primite
        # print(data)

        # Deschide fișierul .csv pentru scriere la final
        with open('IoTData.csv', 'a+', newline='') as file:
            # Folosește ghilimele pentru valori
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)

            # Creeaza un timestamp pentru fiecare rând scris
            datetimeObj = datetime.now()
            timestamp_new = datetimeObj.strftime("%Y-%b-%d %H:%M:%S")
            values.append(timestamp_new)

            # Completează un rând întreg de măsurători
            for property in properties:
                values.append(str(data[property]))

            # Scrie rândul respectiv pe un alt rând din fișierul .csv
            writer.writerow(values)
            # Golește rândul pentru următoarea iterație
            # Dacă nu este apelată funcția clear(), fișierul ar conține același rând de măsurători în continuu
            values.clear()
        yield data, addr
