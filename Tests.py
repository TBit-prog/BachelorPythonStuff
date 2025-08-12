from dataclasses import dataclass
from time import sleep

@dataclass
class usb_stuff:
    wert1 : int
    wert2 : int

@dataclass
class mqtt_stuff:
    wert1 : int
    wert2 : int


@dataclass 
class context:
    mqtt_stuff : mqtt_stuff
    usb_stuff  : usb_stuff


class State:
    def __init__(self, context):
        self.context = context
        
    def next(self):
        pass

class StateMachine:
    def __init__(self, context):
        self.context = context
        self.State = StateOne(context)
    
    def run(self):
        print("State Machine gestartet.")
        while True:
            self.State = self.State.next()

            
class StateOne(State):
    def __init__(self, context):
        self.context = context
        self.usb     = context.usb_stuff

    def print_test(self):
        print(self.usb.wert1)

    def next(self):
        print("Bin in Zustand eins")
        sleep(2)
        return StateTwo(self.context)


class StateTwo(State):
    def __init__(self, context):
        self.context = context

    def next(self):
        print("Bin in Zustand zwei")
        sleep(2)
        return StateOne(self.context)





if __name__  == "__main__":
    usb1 = usb_stuff(2,3)
    mqtt1 = mqtt_stuff(4,5)
    context1 = context(usb1, mqtt1)


    status1 = StateOne(context1)
    status2 = StateTwo(context1)
    sm      = StateMachine(context1)

    sm.run()
