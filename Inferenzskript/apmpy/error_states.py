from apmpy.loop_states import State
from time import sleep
import sys

# Model Error Class
class ModelError(State):
    def __init__(self, context):
        self.context = context
    
    def next(self):
        print("Fehler beim Laden des Modells")
        self.context.error.print_error()
        self.context.error.reset_error()
        print("Das Programm wird beendet.")
        sys.exit(0)


# USB Connect Error Class
class USBConnectError(State):
    def __init__(self, context):
        self.context = context
    
    def next(self):
        from apmpy.connection_states import USBConnect
        print("Fehler bei der USB Verbindung")
        self.context.error.print_error()
        self.context.error.reset_error()
        sleep(3)
        return USBConnect(self.context)


# MQTT Connect Error Class
class MQTTConnectError(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        from apmpy.connection_states import MQTTConnect
        print("Fehler bei der MQTT Verbindung")
        self.context.error.print_error()
        self.context.error.reset_error()
        sleep(3)
        return MQTTConnect(self.context)





