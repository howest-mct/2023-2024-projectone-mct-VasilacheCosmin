from RPi import GPIO
import socket
import json
import time

# Nieuwe pinconfiguratie
data_input = 23  # DS
output_enable = 24  # OE (Active LOW)
storage_reg_clck_input = 25  # ST_CP
shift_reg_clck_input = 12  # SH_CP
master_reset = 17  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [6, 13, 19, 26]  # DIG1, DIG2, DIG3, DIG4

# Segmentpatronen voor cijfers 0-9

# Segmentpatronen voor cijfers 0-9
digit_patterns = {
    '0': 0b11111100,
    '1': 0b01100000,
    '2': 0b11011010,
    '3': 0b11110010,
    '4': 0b01100110,
    '5': 0b10110110,
    '6': 0b10111110,
    '7': 0b11100000,
    '8': 0b11111110,
    '9': 0b11110110
}
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(data_input, GPIO.OUT)
    GPIO.setup(output_enable, GPIO.OUT)
    GPIO.setup(storage_reg_clck_input, GPIO.OUT)
    GPIO.setup(shift_reg_clck_input, GPIO.OUT)
    GPIO.setup(master_reset, GPIO.OUT)
    for pin in digit_pins:
        GPIO.setup(pin, GPIO.OUT)

def send_bit():
    GPIO.output(storage_reg_clck_input, GPIO.HIGH)
    GPIO.output(storage_reg_clck_input, GPIO.LOW)

def shift_bits():
    GPIO.output(shift_reg_clck_input, GPIO.HIGH)
    GPIO.output(shift_reg_clck_input, GPIO.LOW)

def init_shift_register():
    GPIO.output(output_enable, GPIO.LOW)
    GPIO.output(master_reset, GPIO.LOW)
    GPIO.output(master_reset, GPIO.HIGH)
    GPIO.output(storage_reg_clck_input, GPIO.HIGH)
    GPIO.output(storage_reg_clck_input, GPIO.LOW)

def write_one_bit(bitje):
    GPIO.output(data_input, bitje)
    shift_bits()

def write_one_byte(bytetje):
    for i in range(8):
        bitjeh = (bytetje >> i) & 1
        write_one_bit(bitjeh)
    send_bit()

def select_digit(digit):
    for i, pin in enumerate(digit_pins):
        GPIO.output(pin, GPIO.LOW if i == digit else GPIO.HIGH)

def display_speed(speed_mps):
    # Converteer snelheid van m/s naar km/h en splits in cijfers
    speed_kmph = speed_mps * 3.6
    speed_str = f"{speed_kmph:05.2f}"  # Formatteer naar 5.2f, bv: "012.34"
    print('dit is de snelheid: ', speed_str)
    
    #if speed_kmph < 10:
    #   speed_str = "0" + speed_str  # Voeg een extra nul toe aan het begin
    
    speed_str = speed_str.replace(".", "")  # Verwijder de punt voor display

    for digit in range(4):
        digit_value = speed_str[digit]
        pattern = digit_patterns[digit_value]
        if digit == 1:  # Voeg decimale punt toe aan het tweede cijfer
            pattern |= 0b00000001
        #print(f"Digit {digit}: {digit_value} - Pattern: {bin(pattern)}")  # Debugging output
        write_one_byte(pattern)
        select_digit(digit)
        time.sleep(0.005)  # Delay for persistence of vision


class GPSClient:
    def __init__(self, host="localhost", port=2947):
        self.host = host
        self.port = port
        self.gpsd_socket = None
        self.connect()

    def connect(self):
        try:
            self.gpsd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.gpsd_socket.connect((self.host, self.port))
            self.gpsd_socket.sendall(b'?WATCH={"enable":true,"json":true}\n')
            print("Connected to gpsd and listening for GPS data...")
        except Exception as e:
            print(f"Could not connect to gpsd: {e}")
            self.gpsd_socket = None

    def receive_data(self):
        if not self.gpsd_socket:
            print("Not connected to gpsd.")
            return None
        try:
            data = self.gpsd_socket.recv(4096)
            if data:
                return data.splitlines()
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def parse_data(self, data):
        for line in data:
            try:
                packet = json.loads(line)
                if packet.get('class') == 'TPV':  # TPV class has the position and velocity information
                    speed = packet.get('speed', "N/A")
                    return speed
            except json.JSONDecodeError:
                pass
            except KeyError:
                pass
        return None

    def cleanup(self):
        if self.gpsd_socket:
            self.gpsd_socket.close()
            print("GPS socket closed.")

def main():
    gps_client = GPSClient()
    setup()
    init_shift_register()

    try:
        while True:
            data = gps_client.receive_data()
            if data:
                speed_mps = gps_client.parse_data(data)
                print(speed_mps)
                if speed_mps is not None:
                    for _ in range(50):  # Multiplexing loop for visibility
                        display_speed(speed_mps)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    finally:
        GPIO.cleanup()
        if gps_client.gpsd_socket:
            gps_client.cleanup()
        print("Script has stopped!!!")

if __name__ == "__main__":
    main()
