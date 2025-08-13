from apmpy.loop_states import State, ReadAPMData

from apmpy.error_states import (
    ModelError,
    USBConnectError,
    MQTTConnectError
)

import serial

# Load Model Class
class LoadRFModel(State):
    """Erster Zustand - Lädt das Model. Im Fehlerfall wird Programm komplett abgebrochen"""
    def __init__(self, context):
        self.context  = context

    def next(self):
        try: 
            rf  = self.context.random_forest_param
            rf.load_model()
            rf.load_features()
            rf.extract_features()
            print("Modell geladen und zur Inferenz bereit.")
            return USBConnect(self.context)
        except (FileNotFoundError, ValueError) as e:
            self.context.error.state_error = e
            return ModelError(self.context)
           

            
# USB Connect Class
class USBConnect(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        usb     = self.context.usb_param
        try:
            usb.ser = usb.connecting()
            print("USB verbindung erfolgreich aufgebaut.")
            return MQTTConnect(self.context)  
        except serial.SerialException as e:
            self.context.error.state_error = e
            return USBConnectError(self.context)    


# MQTT Connect class
class MQTTConnect(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        mqtt  = self.context.mqtt_param
        try:
            mqtt.create_client()
            mqtt.connect()
            print("MQTT verbindung erfolgreich aufgebaut.")
            return ReadAPMData(self.context)
        except (ConnectionError, ValueError, TypeError, OSError) as e:
            self.context.error.state_error = e
            return MQTTConnectError(self.context)
