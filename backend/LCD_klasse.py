import RPi.GPIO as GPIO
import smbus2
import time


class LCD:
    def __init__(self, parRS=21, parE=20, i2c_address=0x38):
        # GPIO pin assignments
        self.RS = parRS
        self.E = parE

        # I2C setup
        self.bus = smbus2.SMBus(1)
        self.address = i2c_address

        # Initialize GPIO
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)

        self.init_LCD()

    def pulse_enable(self):
        GPIO.output(self.E, GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.0005)

    def send_instruction(self, value):
        GPIO.output(self.RS, GPIO.LOW)
        self.bus.write_byte(self.address, value)
        self.pulse_enable()

    def send_character(self, value):
        GPIO.output(self.RS, GPIO.HIGH)
        self.bus.write_byte(self.address, value)
        self.pulse_enable()

    def init_LCD(self):
        # Initialize LCD
        self.send_instruction(0b00110000)  # Function set: 8-bit mode, 2 lines, 5x8 font
        time.sleep(0.05)
        self.send_instruction(0b00110000)  # Function set: 8-bit mode, 2 lines, 5x8 font
        time.sleep(0.005)
        self.send_instruction(0b00110000)  # Function set: 8-bit mode, 2 lines, 5x8 font
        time.sleep(0.005)
        self.send_instruction(0b00111000)  # Function set: 8-bit mode, 2 lines, 5x8 font
        time.sleep(0.005)
        self.send_instruction(
            0b00001100
        )  # Display control: Display on, cursor off, blink off
        time.sleep(0.005)
        self.send_instruction(0b00000001)  # Clear display
        time.sleep(0.005)
        self.send_instruction(
            0b00000110
        )  # Entry mode set: Increment cursor, no display shift
        time.sleep(0.005)

    def clear_display(self):
        self.send_instruction(0b00000001)  # Clear display
        time.sleep(0.005)

    def write_message(self, message, line=1):
        if line == 1:
            self.send_instruction(0b10000000)  # Set cursor to first line
        elif line == 2:
            self.send_instruction(0b11000000)  # Set cursor to second line
        else:
            raise ValueError("Line must be 1 or 2")

        for char in message:
            self.send_character(ord(char))
