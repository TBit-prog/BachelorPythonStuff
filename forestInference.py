# Datastuff
from dataclasses import dataclass
import numpy as np
import pandas as pd
from json import split, loads

# Connection imports
import serial
from paho.mqtt import client as mqtt_client

#Random Forest Imports
import joblib


# Dataclass Connection Param, mit frozen=True wird verhidnert, dass Daten in Klasse verändert werden
@dataclass
class USBParam(frozen = True):
    """Beinhaltet alle Parameter und Methoden für die USB Verbindung."""
    ser             : serial.Serial         
    usbdata         : str                   
    baudrate        : int            
    comport         : str

    def connecting(self):
        self.ser     = serial.Serial(
            port     = self.comport, 
            baudrate = self.baudrate,
            parity   = serial.PARITY_EVEN,
            rtscts   = 1                        #Request to send und clear to send aktivieren
            )
        return self.ser

    def send_trigger(self):
        self.ser.write(b"G\n") # Im APM ist G der Trigger, um eine Antwort zu erhalten

    def read_data(self):
        self.usbdata = self.ser.readline().decode("utf-8").strip()

    def raise_error(self):
        pass
    

@dataclass
class MQTTParam(frozen = True):
    """Beinhaltet alle Parameter und Methoden für die MQTT Verbindung."""
    port            : int
    topic           : str 
    qos             : int                   = None
    user_name       : str                   = None
    user_password   : str                   = None
    brokername      : str
    mqtt_message    : str                   
    client          : mqtt_client.Client    
    client_id       : str                   = None

    def create_client(self):
        self.client = mqtt_client.Client(
            mqtt.CallbackAPIVersion.VERSION2, 
            client_id = self.client_id
            )
        
    def connect(self):
        self.client.connect(
        host = self.brokername,
        port = self.port                  
        )

    def raiser_error(self):
        pass


# Dataclass Main Loop Param
@dataclass
class MainLoopParam:
    """Beinhaltet die transferierten Daten und Methoden zu deren Aufbereitung."""
    raw_data        : str 
    processed_data  : str
    temperatur      : float
    humidity        : float
    volume          : float
    iaq             : int 

    def json_formatting(self, data):
        self.raw_data       = data.split('"UniqueId":"0x287681FFFEE2AFEA",')[-1] #Unique ID ausschneiden
        self.raw_data       = "{" + self.raw_data # JSON Format vervollständigen
        self.processed_data = json.loads(self.raw_data) 

    def get_apm_data(self):


# Dataclass Model Param
@dataclass
class RandomForestParam:
    """Beinhaltet die nötigen Parameter und Methoden des Random Forest Modells."""
    #Input daten als Tupel übergeben?
    rf_input               : pd.DataFrame
    rf_output              : str
    model_path             : str            
    model                  : joblib

    def load_model(self):
        self.model = joblib.load(self.model_path)

    def infere(self):
        self.rf_output = self.model.predict(self.rf_input)


# Context Dataclass
@dataclass
class Context:
    """Bündelt die restlichen Dataclasses, damit Übergabe vereinheitlicht wird und Erweiterbarkeit und Wartbarkeit verbessert werden."""
    usb_param        : USBParam
    mqtt_param       : MQTTParam
    main_param       : MainLoopParam
    model_param      : RandomForestParam


# State Class
class State:
    """State Class, die notwendig ist, um State Machine aufzusetzen. Hier ist der Context gleich enthalten. Also muss man keine Dataklassen extra übergeben."""
    def next(self, context : Context):
        pass

    def error_path(self, context : Context):
        pass


# USB Connect Class
class USBConnect(State):


# USB Connect Error Class
class USBConnectError(State):


# MQTT Connect class
class MQTTConnect(State):


# MQTT Connect Error Class
class MQTTConnectError(State):


# APM Data Aquisition Class
class ReadAPMData(State):


# Model Inference Class
class InferenceData(State):


# Model Error Class
class ModelError(State):


# MQTT Send Class
class SendData(State):
    

