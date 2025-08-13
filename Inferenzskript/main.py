"""Datenklassen importieren."""
from apmpy.data import (
    USBParam, 
    MQTTParam, 
    DataProcessParam, 
    RandomForestParam, 
    Error,
    Context

)

"""Zustände der Statemachine importieren."""
from apmpy.connection_states import (
    LoadRFModel,
    USBConnect,
    MQTTConnect
)

from apmpy.loop_states import (
    State,
    StateMachine,
    ReadAPMData,
    ProcessAPMData,
    InfereData,
    SendData
)

from apmpy.error_states import (
    ModelError,
    USBConnectError,
    MQTTConnectError
)

"""Weitere Importe."""
import paho.mqtt.publish as publish
from time import sleep

#__________________________________________________________________________________________________________________________________________  
"""
In diesem Abschnitt werden alle Parameter 
für MQTT und USB Verbindung sowie der Speicherort des Modells definiert
"""

model_path   = r"C:\Users\Jeuh\Desktop\Projektdaten lokal\03_Edge-Platform - Bachelorprojekt\Software\KI-Modelle\Modelle\Random Forest"
model_name   = r"\MyFirstForest.joblib"
feature_name = r"\MyFeatureNames.joblib"

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
    model_path    = model_path + model_name,
    feature_path  = model_path + feature_name
)

state_error = Error(
    topic_error         = "Error Output"
)

context = Context(
    usb_param           = usb_param,
    mqtt_param          = mqtt_param,
    data_process_param  = data_process_param,
    random_forest_param = random_forest_param,
    error               = state_error
)
#__________________________________________________________________________________________________________________________________________
"""Hier wird die Statemachine gestartet"""

if __name__ == "__main__":
    sm = StateMachine(context)
    sm.run()
