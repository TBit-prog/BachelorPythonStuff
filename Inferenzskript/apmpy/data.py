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
import paho
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
            timeout  = 1,
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
    iaq             : float     = None


    def json_formatting(self, usb_data):
        self.raw_data       = usb_data
        self.processed_data = json.loads(self.raw_data) 

    def extract_data(self):
        self.temperature      = self.processed_data["TMP"]["Value"]
        self.humidity         = self.processed_data["HUM"]["Value"]
        self.iaq              = self.processed_data["IAQ"]["Value"]

    def get_data(self, usb_data):
        self.json_formatting(usb_data)
        self.extract_data()


# Dataclass Model Param
@dataclass
class RandomForestParam:
    """Beinhaltet die nötigen Parameter und Methoden des Random Forest Modells."""
    model_path             : str
    feature_path           : tuple
    features               : tuple      = None      
    model                  : joblib     = None
    rf_input               : np.array   = None
    rf_output              : int        = None

    def extract_features(self):
        """Sicherstellen, dass Features in richtiger Reihenfolge und in"""
        self.features = self.features[0:3]

    def arrange_features(self):
        arr = np.array(self.rf_input).reshape(1, -1)
        self.rf_input = pd.DataFrame(arr, columns=self.features)

    def load_model(self):
        self.model = joblib.load(self.model_path)

    def load_features(self):
        self.features = joblib.load(self.feature_path)

    def infere(self):
        self.arrange_features()
        self.rf_output = self.model.predict(self.rf_input)


@dataclass
class Error:
    """Errorklasse, die den Fehler beinhaltet""" 
    topic_error    : str                #Falls man error Stream über MQTT realisieren will
    state_error    : Exception = None

    def print_error(self):
        print(f"Exception: {self.state_error}")
        print(f"Typ: {type(self.state_error)}")
        print(f"Args: {self.state_error.args}")

    def reset_error(self):
        self.state_error = None


@dataclass
class Context:
    """Bündelt die restlichen Dataclasses, damit Übergabe vereinheitlicht wird und Erweiterbarkeit und Wartbarkeit verbessert werden."""
    usb_param           : USBParam
    mqtt_param          : MQTTParam
    data_process_param  : DataProcessParam
    random_forest_param : RandomForestParam
    error               : Error


