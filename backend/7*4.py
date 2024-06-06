from RPi import GPIO
import time
from datetime import datetime

# Nieuwe pinconfiguratie
data_input = 25  # DS
output_enable = 12  # OE (Active LOW)
storage_reg_clck_input = 16  # ST_CP
shift_reg_clck_input = 20  # SH_CP
master_reset = 21  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [5, 6, 13, 19]  # DIG1, DIG2, DIG3, DIG4


"""# Nieuwe pinconfiguratie
data_input = 23  # DS
output_enable = 24  # OE (Active LOW)
storage_reg_clck_input = 25  # ST_CP
shift_reg_clck_input = 12  # SH_CP
master_reset = 17  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [6, 13, 19, 26]  # DIG1, DIG2, DIG3, DIG4"""



# 
# DS 23
# OE 24
# ST_CP 25
# SH_CP 12
# MR 17


#DIG PIN
#6
#13
#19
#26

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

def display_time(hour, minute):
    # Omzetten naar string en opvullen met nullen
    time_str = f"{hour:02}{minute:02}"
    
    for digit in range(4):
        print(digit_patterns[time_str[digit]])
        write_one_byte(digit_patterns[time_str[digit]])
        select_digit(digit)
        time.sleep(0.005)  # Delay for persistence of vision

setup()
init_shift_register()

try:
    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute
 
        display_time(hour, minute)
        #time.sleep(1)

except KeyboardInterrupt as e:
    print(e)

finally:
    GPIO.cleanup()

print("Script has stopped!!!")
