# Datastuff
from dataclasses import dataclass
import numpy as np
import pandas as pd
import json

# Connection imports
import serial
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#Random Forest Imports
import joblib

#Misc Stuff
from time import sleep



# Dataclass Connection Param, mit frozen=True wird verhidnert, dass Daten in Klasse verändert werden
@dataclass
class USBParam():
    """Beinhaltet alle Parameter und Methoden für die USB Verbindung.""" 
    baudrate        : int            
    comport         : str
    ser             : serial.Serial  = None       
    usbdata         : str            = None

    def connecting(self):
        self.ser     = serial.Serial(
            port     = self.comport, 
            baudrate = self.baudrate,
            timeout  = 0,
            parity   = serial.PARITY_EVEN,
            rtscts   = 1                        #Request to send und clear to send aktivieren
            )
        return self.ser

    def send_trigger(self):
        self.ser.write(b"G\n") # Im APM ist G der Trigger, um eine Antwort zu erhalten
        sleep(1)

    def read_data(self):            
        self.usbdata = self.ser.readline().decode("utf-8").strip()
        print(f"Daten:\n{self.usbdata}")


    def check_port(self):
        if self.ser.is_open:
            print("Port ist geöffnet.")
        else:
            print("Port ist geschlossen.")

    def raise_error(self):
        pass
    

@dataclass
class MQTTParam():
    """Beinhaltet alle Parameter und Methoden für die MQTT Verbindung."""
    port              : int                 #int oder str?
    topic_raw         : str 
    topic_inference   : str
    brokername        : str
    host              : str
    client            : mqtt_client.Client    = None
    message_raw       : str                   = None
    message_inference : int                   = None    
    client_id         : str                   = None
    qos               : int                   = None
    user_name         : str                   = None
    user_password     : str                   = None

    def create_client(self):
        self.client = mqtt_client.Client(mqtt.CallbackAPIVersion.VERSION2, client_id = "TestUser")
        
    def connect(self):
        self.client.connect(
        host = self.host,
        port = self.port                  
        )

    def raiser_error(self):
        pass


# Dataclass Main Loop Param
@dataclass
class DataProcessParam:
    """Beinhaltet die transferierten Daten und Methoden zu deren Aufbereitung."""
    raw_data        : str       = None
    processed_data  : str       = None
    temperature     : float     = None
    humidity        : float     = None
    volume          : float     = None
    iaq             : int       = None
    split_string    : str       = None


    def json_formatting(self):
        self.raw_data       = self.raw_data.split('"UniqueId":"0x287681FFFEE2AFEA",')[-1] #Unique ID ausschneiden
        self.raw_data       = "{" + self.raw_data # JSON Format vervollständigen
        self.processed_data = json.loads(self.raw_data) 

    def extract_data(self):
        self.temperature      = self.processed_data["TMP"]["Value"]
        self.humidity         = self.processed_data["HUM"]["Value"]
        self.volume           = self.processed_data["VOL"]["Value"]
        self.iaq              = self.processed_data["IAQ"]["Value"]

    def get_data(self):
        self.json_formatting()
        self.ectract_data()


# Dataclass Model Param
@dataclass
class RandomForestParam:
    """Beinhaltet die nötigen Parameter und Methoden des Random Forest Modells."""
    #Input daten als Tupel übergeben?
    model_path             : str            
    model                  : joblib     = None
    rf_input               : np.array   = None
    rf_output              : int        = None

    def load_model(self):
        self.model = joblib.load(self.model_path)

    def infere(self):
        self.rf_output = self.model.predict(self.rf_input)

    def setup_data(self):
        pass


# Context Dataclass
@dataclass
class Context:
    """Bündelt die restlichen Dataclasses, damit Übergabe vereinheitlicht wird und Erweiterbarkeit und Wartbarkeit verbessert werden."""
    usb_param           : USBParam
    mqtt_param          : MQTTParam
    data_process_param  : DataProcessParam
    random_forest_param : RandomForestParam


# State Class
class State:
    """
    State Class, die notwendig ist, um State Machine aufzusetzen. Hier ist der Context gleich enthalten. 
    Also muss man keine Dataklassen extra übergeben.
    """
    def __init__(self, context):
        self.context = context

    def next(self, context):
        pass

    def error_path(self, context):
        pass

class StateMachine:
    """State Machine Klasse, welche jeweils die next() Funktion der einzelnen Zustände aufruft - und somit den Ablauf steuert"""
    def __init__(self, context):
        self.context = context
        self.State   = LoadRFModel(context) 

    def run(self):
        print("State Machine gestartet.")
        while True:
            self.State = self.State.next()


# Load Model Class
class LoadRFModel(State):
    """Erster Zustand - Lädt das Model. Im Fehlerfall wird Programm komplett abgebrochen"""
    def __init__(self, context):
        self.context  = context

    def next(self):
        print("Modell geladen und zur Inferenz bereit.")
        rf  = self.context.random_forest_param
        rf.load_model()
        return USBConnect(self.context)


# USB Connect Class
class USBConnect(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        usb     = self.context.usb_param
        usb.ser = usb.connecting()
        print("USB verbindung erfolgreich aufgebaut.")
        return MQTTConnect(self.context)        


# USB Connect Error Class
class USBConnectError(State):
    def __init__(self, context):
        self.context = context

# MQTT Connect class
class MQTTConnect(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        mqtt  = self.context.mqtt_param
        mqtt.create_client()
        mqtt.connect()
        print("MQTT verbindung erfolgreich aufgebaut.")
        return ReadAPMData(self.context)

# MQTT Connect Error Class
class MQTTConnectError(State):
    pass

# APM Data Aquisition Class
class ReadAPMData(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        usb = self.context.usb_param
        usb.send_trigger()
        print("Trigger gesendet")
        usb.check_port()
        sleep(2)
        usb.read_data()
        print("APM Daten gelesen")
        return ProcessAPMData(self.context)


#Processing Dataclass
class ProcessAPMData(State):
    def __init__(self, context):
        self.context = context
    
    def next(self):
        process = self.context.data_process_param
        process.get_data()
        print("APM Daten verarbeitet.")
        return SendData(self.context)

# Model Inference Class
class InferenceData(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        rf  = self.context.random_forest_param
        rf.infere(self)
        print("Inferenz durchgeführt.")
        return SendData(self.context)

# Model Error Class
class ModelError(State):
    pass

# MQTT Send Class
class SendData(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        topic_raw       = self.context.mqtt_param.topic_raw
        topic_inference = self.context.mqtt_param.topic_inference
        host            = self.context.mqtt_param.host 
        port            = self.context.mqtt_param.port
        apm_data        = self.context.data_process_param.raw_data
        inference_data  = self.context.random_forest_param.rf_output
        #Sende unverarbeiteten JSON
        publish.single(
            topic    = topic_raw,
            payload  = apm_data,
            hostname = host,
            port     = port
            )
        #Sende inferenzoutput des RF Modells
        publish.single(
            topic    = topic_inference,
            payload  = inference_data,
            hostname = host,
            port     = port
        )
        print("Daten an MQTT Broker gesendet.")
        return ReadAPMData(self.context)
    


#_____________________________________________________________
model_path = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Modelle\Random Forest"
model_name = r"\MyFirstForest.joblib"

usb_param = USBParam(
    baudrate = 115200,
    comport  = "COM5"
)

mqtt_param = MQTTParam(
    port            = 1883,
    topic_raw       = "APM",
    topic_inference = "Inferenz",
    brokername      = "Mosquitto",
    host            = "localhost"
)

data_process_param = DataProcessParam()

random_forest_param = RandomForestParam(
    model_path = model_path + model_name
)

context = Context(
    usb_param           = usb_param,
    mqtt_param          = mqtt_param,
    data_process_param  = data_process_param,
    random_forest_param = random_forest_param
)

if __name__ == "__main__":
    sm = StateMachine(context)
    sm.run()
