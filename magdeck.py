import serial
import serial.tools.list_ports
import re

class MagDeck():
    def __init__(self):
        self.port = MagDeck.find_mag_deck()

    def _send(self, command, data_len=70, timeout=0.2):
        if not self.port:
            # Try connect again
            self.port = MagDeck.find_mag_deck()
            if not self.port:
                return None

        s = ""
        try:
            with serial.Serial(self.port, 115200 , timeout=timeout) as ser:
                ser.write(bytes(command, 'utf8')+b'\r\n') 
                s = ser.read(data_len).decode()      # read up to ten bytes (timeout)
        except serial.serialutil.SerialException:
            return None

        return s

    def home(self):

        s = self._send('G28.2', data_len=8, timeout=20)

        if s:
            return True
        else:
            return None

    def move(self, mm):

        s = self._send(f'G0 Z{mm}', data_len=8, timeout=20)

        if s:
            return True
        else:
            return None

    def get_position(self):

        s = self._send('M114.2')

        if s:
            s = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", s)
            return float(s[0])
        else:
            return None

    
    def probe_plate(self):

        self._send('G38.2', data_len=8,timeout=20)
        return self.get_plate_position()


    def get_plate_position(self):

        s = self._send('M836')

        if s:
            s = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", s)
            s = float(s[0])
            if s == 25.0:
                return None
            else:
                return s
        else:
            return None

    def move_to_plate(self):
        pos = self.get_plate_position()
        if pos:
            if self.move(pos):
                return True
            else:
                return None
        else:
            return None

    def get_info(self):
        info = self._send('M115', data_len=100, timout=0.5)

        if info:
            return info
        else: 
            return ""

    @staticmethod
    def list_ports():
        ports = [desc.usb_description() for desc in serial.tools.list_ports.comports()]
        return ports

    @staticmethod
    def find_mag_deck():
        ports = MagDeck.list_ports()
        mag_port = ''
        for p in ports:

            with serial.Serial(p, 115200 , timeout=0.5) as ser:
                ser.write(b'M115\r\n') 
                s = ser.read(100).decode()      # read up to ten bytes (timeout)
                if 'serial:MDV' in s:
                    mag_port = p
                    break
        
        return mag_port


def connect():
    ser = serial.Serial('/dev/ttyUSB0')  


if __name__ == "__main__":
    deck = MagDeck()
    p = deck.get_plate_position()