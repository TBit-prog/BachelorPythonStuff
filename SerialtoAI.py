import tensorflow as tf
import numpy as np
import paho.mqtt.publish as publish
import serial
import serial.tools.list_ports as port_list
import time
import json


ports = list(port_list.comports())

for p in ports:
    print(p)

# Modell laden
modelpath = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Modelle\NN\Window_Open_90.keras"
model = tf.keras.models.load_model(modelpath)

#MQTT Parameter
BROKER = "ie-databus"   
COMPORT = "/dev/ttyACM0"
BAUDRATE = 115200
TOPIC = "MyTopic"
NAME = "edge"
PW   = "edge"

#Eigenschaften des seriellen Ports
ser = serial.Serial('COM5', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
G = b"G"
ser.write(b"G\n")
s = ser.readline().decode("utf-8").strip()

while True:
    ser.write(b"G\n")
    time.sleep(2)
    if ser.inWaiting() > 0:
        response = ser.readline().decode("utf-8").strip()

    #JSON Formatieren
    json_str = response.split('"UniqueId":"0x287681FFFEE2AFEA",')[-1]
    json_complete = "{" + json_str
    data = json.loads(json_complete)
    #Daten extrahieren
    Temp = data["TMP"]["Value"]
    IAQ = data["IAQ"]["Value"] 
    Volume = data["VOL"]["Value"]
    Hum = data["HUM"]["Value"]
    VOC = data["VOC"]["Value"]

    #Daten in ein numpy Array umwandeln
    daten = np.array([[Temp, IAQ, Volume, Hum, VOC]])

    # Vorhersage machen
    vorhersage = model.predict(daten)
    # Vorhersage in ein lesbares Format umwandeln
    #vorhersage = round(vorhersage[0][0], 0) 

    #print(f"Daten: {daten}")
    #Gebe das Ergebnis und die Messdaten aus
    print(f"Temperatur: {Temp}, IAQ: {IAQ}, Volume: {Volume}, Humidity: {Hum}, VOC: {VOC}")
    print(vorhersage)