import serial
from dataclasses import dataclass
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


usb = USBParam(
    baudrate = 115200,
    comport  = "COM5"
)

usb.ser = usb.connecting()
print("Verbindung erfolgreich")
usb.send_trigger()
print("Trigger gesendet")
sleep(2)
if usb.ser.inWaiting() > 0:
    usbdata = usb.ser.readline().decode("utf-8").strip()
print(f"Daten:\n{usbdata}")
print(usb.usbdata)