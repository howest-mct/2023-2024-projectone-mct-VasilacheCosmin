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

    def display_speed(self, speed_mps):
        # Converteer snelheid van m/s naar km/h en splits in cijfers
        speed_kmph = speed_mps * 3.6
        speed_str = f"{speed_kmph:05.2f}"  # Formatteer naar 5.2f, bv: "012.34"
        print('dit is de snelheid: ', speed_str)
        
        speed_str = speed_str.replace(".", "")  # Verwijder de punt voor display

        for digit in range(4):
            digit_value = speed_str[digit]
            pattern = self.digit_patterns[digit_value]
            if digit == 1:  # Voeg decimale punt toe aan het tweede cijfer
                pattern |= 0b00000001
            #print(f"Digit {digit}: {digit_value} - Pattern: {bin(pattern)}")  # Debugging output
            self.write_one_byte(pattern)
            # print(pattern)
            # print(digit)
            self.select_digit(digit)
            time.sleep(0.005)  # Delay for persistence of vision

    def clear_display(self):
        for digit in range(4):
            self.write_one_byte(0b00000000)
            self.select_digit(digit)
            time.sleep(0.005)

    def cleanup(self):
        self.clear_display()
        # Specifieke pinnen opruimen
        used_pins = [self.data_input, self.output_enable, self.storage_reg_clck_input, self.shift_reg_clck_input, self.master_reset] + self.digit_pins
        for pin in used_pins:
            GPIO.setup(pin, GPIO.IN)

if __name__ == "__main__":
    display = SevenSegmentDisplay()

    # Lijst van gesimuleerde snelheden in m/s
    simulated_speeds_mps = [
        10.23, 0.062, 0.062, 0.062, 0.062, 1.228, 1.709, 2.001,
        1.788, 1.334, 1.095, 0.693, 0.271, 0.301, 0.247, 0.122, 0.068, 0.066,
        0.055, 0.13, 0.038, 0.076, 0.061, 0.083, 0.146, 0.097, 0.09, 0.128,
        0.034, 0.035
    ]

    try:
        while True:
            display.write_one_byte(0b11111111)
            time.sleep(1)
            print(1)
            display.write_one_byte(0)
            time.sleep(1)
            print(2)

            # for speed_mps in simulated_speeds_mps:
            #     for x in range(50):
            #         display.display_speed(speed_mps)
            #     #time.sleep(1)  # Delay before showing the next speed

    except KeyboardInterrupt as e:
        print(e)

    finally:
        GPIO.cleanup()

    print("Script has stopped!!!")
