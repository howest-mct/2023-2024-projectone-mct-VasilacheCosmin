import time
import RPi.GPIO as GPIO

# Define the pins 23-24-25-12-17
ds_pin = 23
oe_pin = 24
stcp_pin = 25
shcp_pin = 12
mr_pin = 17

digitPins = [ 13, 6,26, 19]  # Pinnen verbonden met de digitale pinnen van de 7-segment display





# Define the 74HC595 class
class ShiftRegister:
    def __init__(self, data_pin, shiftclockpulse_pin, storageclockpulse_pin, masterreset_pin, outputenable_pin):
        self.data_pin = data_pin
        self.shiftclockpulse_pin = shiftclockpulse_pin
        self.storageclockpulse_pin = storageclockpulse_pin
        self.masterreset_pin = masterreset_pin
        self.outputenable_pin = outputenable_pin
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.shiftclockpulse_pin, GPIO.OUT)
        GPIO.setup(self.storageclockpulse_pin, GPIO.OUT)
        GPIO.setup(self.masterreset_pin, GPIO.OUT)
        GPIO.setup(self.outputenable_pin, GPIO.OUT)
        for pin in digitPins:
            GPIO.setup(pin, GPIO.OUT)

    def init_shift_register(self):
        GPIO.output(self.masterreset_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.masterreset_pin, GPIO.HIGH)
        GPIO.output(self.outputenable_pin, GPIO.LOW)

    def write_one_bit(self, bit):
        GPIO.output(self.data_pin, bit)
        GPIO.output(self.shiftclockpulse_pin, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.shiftclockpulse_pin, GPIO.HIGH)

    def write_one_byte(self, data_byte):
        for i in range(8):
            bit = (data_byte >> i) & 1
            self.write_one_bit(bit)
        time.sleep(0.001)

    def copy_to_storage_register(self):
        GPIO.output(self.storageclockpulse_pin, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.storageclockpulse_pin, GPIO.HIGH)

    def reset(self):
        self.write_one_byte(0b11111111)
        self.copy_to_storage_register()
        time.sleep(0.3)

# Segmentcodes voor de cijfers 0-9 op een 7-segment display
digit_segments = {
    0: 0b00111111,  # Cijfer 0
    1: 0b00000110,  # Cijfer 1
    2: 0b01011011,  # Cijfer 2
    3: 0b01001111,  # Cijfer 3
    4: 0b01100110,  # Cijfer 4
    5: 0b01101101,  # Cijfer 5
    6: 0b01111101,  # Cijfer 6
    7: 0b00000111,  # Cijfer 7
    8: 0b01111111,  # Cijfer 8
    9: 0b01101111,  # Cijfer 9
}

# Functie om de omgekeerde counter weer te geven op de 7-segment display
def display_counter(shift, start_digit):
    digits = [(start_digit - i) % 10 for i in range(4)]

    for i in range(4):
        GPIO.output(digitPins[i], GPIO.HIGH)  # Deactivate all digits
    for i in range(4):
        shift.write_one_byte(digit_segments[digits[i]])
        shift.copy_to_storage_register()
        GPIO.output(digitPins[i], GPIO.LOW)  # Activate the current digit
        time.sleep(1)  # Small delay to ensure the digit is displayed
        GPIO.output(digitPins[i], GPIO.HIGH)  # Deactivate the current digit

# Functie om de counter te updaten
def update_counter(shift, start_digit):
    display_counter(shift, start_digit)

try:
    GPIO.cleanup()
    time.sleep(0.2)
    shift = ShiftRegister(ds_pin, shcp_pin, stcp_pin, mr_pin, oe_pin)
    shift.init_shift_register()
    time.sleep(2)

    start_digit = 9
    position = 0
    while True:
        update_counter(shift, start_digit)
        start_digit = (start_digit - 1) % 10  # Decrement the start digit, wrap around at 0
        time.sleep(1)  # Wait 1 second before updating the display

except KeyboardInterrupt:
    shift.reset()
    time.sleep(0.3)
    GPIO.cleanup()
