from RPi import GPIO
import time

class SevenSegmentDisplay:
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

    def __init__(self):
        self.data_input = 23  # DS
        self.output_enable = 24  # OE (Active LOW)
        self.storage_reg_clck_input = 25  # ST_CP
        self.shift_reg_clck_input = 12  # SH_CP
        self.master_reset = 17  # MR (Active LOW)

        self.digit_pins = [6, 13, 19, 26]  # DIG1, DIG2, DIG3, DIG4

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_input, GPIO.OUT)
        GPIO.setup(self.output_enable, GPIO.OUT)
        GPIO.setup(self.storage_reg_clck_input, GPIO.OUT)
        GPIO.setup(self.shift_reg_clck_input, GPIO.OUT)
        GPIO.setup(self.master_reset, GPIO.OUT)
        for pin in self.digit_pins:
            GPIO.setup(pin, GPIO.OUT)
        self.init_shift_register()

    def send_bit(self):
        GPIO.output(self.storage_reg_clck_input, GPIO.HIGH)
        GPIO.output(self.storage_reg_clck_input, GPIO.LOW)

    def shift_bits(self):
        GPIO.output(self.shift_reg_clck_input, GPIO.HIGH)
        GPIO.output(self.shift_reg_clck_input, GPIO.LOW)

    def init_shift_register(self):
        GPIO.output(self.output_enable, GPIO.LOW)
        GPIO.output(self.master_reset, GPIO.LOW)
        GPIO.output(self.master_reset, GPIO.HIGH)
        GPIO.output(self.storage_reg_clck_input, GPIO.HIGH)
        GPIO.output(self.storage_reg_clck_input, GPIO.LOW)

    def write_one_bit(self, bitje):
        GPIO.output(self.data_input, bitje)
        self.shift_bits()

    def write_one_byte(self, bytetje):
        for i in range(8):
            bitjeh = (bytetje >> i) & 1
            self.write_one_bit(bitjeh)
        self.send_bit()

    def select_digit(self, digit):
        for i, pin in enumerate(self.digit_pins):
            GPIO.output(pin, GPIO.LOW if i == digit else GPIO.HIGH)

    def display_test(self):
        for pattern in self.digit_patterns.values():
            for digit in range(4):
                self.write_one_byte(pattern)
                self.select_digit(digit)
                time.sleep(0.5)

    def cleanup(self):
        self.clear_display()
        used_pins = [self.data_input, self.output_enable, self.storage_reg_clck_input, self.shift_reg_clck_input, self.master_reset] + self.digit_pins
        for pin in used_pins:
            GPIO.setup(pin, GPIO.IN)

if __name__ == "__main__":
    display = SevenSegmentDisplay()

    try:
        while True:
            display.display_test()
    except KeyboardInterrupt as e:
        print(e)
    finally:
        display.cleanup()

    print("Script has stopped!!!")
