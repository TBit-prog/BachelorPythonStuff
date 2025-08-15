import paho.mqtt.publish as publish
import numpy as np
import json
import serial
from time import sleep

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
        from apmpy.connection_states import LoadRFModel     #Import muss hier geschehen, weil sonst ein Circular Import Error zu "connection_states.py" vorliegt
        self.context = context
        self.State   = LoadRFModel(context) 

    def run(self):
        print("State Machine gestartet.")
        while True:
            self.State = self.State.next()
            sleep(1)
#####################################################################################################################################################
#####################################################################################################################################################


class ReadAPMData(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        try:
            usb = self.context.usb_param
            usb.send_trigger()
            print("Trigger gesendet")
            usb.check_port()
            usb.read_data()
            print("APM Daten gelesen")
            return ProcessAPMData(self.context)
        except serial.SerialException as e:
            from apmpy.connection_states import USBConnectError
            self.context.error.state_error = e
            return USBConnectError(self.context)

class ProcessAPMData(State):
    def __init__(self, context):
        self.context = context
    
    def next(self):
        process = self.context.data_process_param
        usb_data = self.context.usb_param.usbdata
        data     = self.context.data_process_param
        process.get_data(usb_data)
        print("APM Daten verarbeitet.")
        print(f"Temp {self.context.data_process_param.temperature}")
        self.context.random_forest_param.rf_input = np.array([[data.temperature, data.iaq, data.humidity]])#, data.volume
        print(f"RF_Input nach dataprocessing:{self.context.random_forest_param.rf_input}")
        return InfereData(self.context)


class InfereData(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        print(f"RF_input: {self.context.random_forest_param.rf_input}")
        rf  = self.context.random_forest_param
        rf.infere()
        print("Inferenz durchgeführt.")
        return SendData(self.context)


class SendData(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        try:
            topic_raw       = self.context.mqtt_param.topic_raw
            topic_inference = self.context.mqtt_param.topic_inference
            host            = self.context.mqtt_param.host 
            port            = self.context.mqtt_param.port
            apm_data        = self.context.data_process_param.raw_data
            inference_data  = self.context.random_forest_param.rf_output
            #Sende unverarbeiteten JSON
            publish.single(
                topic    = topic_raw,
                payload  = json.dumps(self.context.data_process_param.raw_data),
                hostname = host,
                port     = port
                )
            print("APM Daten an MQTT Broker gesendet")
            #Sende inferenzoutput des RF Modells
            publish.single(
                topic    = topic_inference,
                payload  = int(self.context.random_forest_param.rf_output),
                hostname = host,
                port     = port
            )
            print("Inferenz an MQTT Broker gesendet.")
            return ReadAPMData(self.context)
        except (ConnectionError, ValueError, TypeError, OSError) as e:
            from apmpy.connection_states import MQTTConnectError
            self.context.error.state_error = e
            return MQTTConnectError(self.context)
    
