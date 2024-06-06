from RPi import GPIO
import time

"""
# Nieuwe pinconfiguratie
data_input = 23  # DS
output_enable = 24  # OE (Active LOW)
storage_reg_clck_input = 25  # ST_CP
shift_reg_clck_input = 12  # SH_CP
master_reset = 17  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [5,6, 13, 19]  # DIG1, DIG2, DIG3, DIG4"""


# Nieuwe pinconfiguratie
data_input = 23  # DS
output_enable = 24  # OE (Active LOW)
storage_reg_clck_input = 25  # ST_CP
shift_reg_clck_input = 12  # SH_CP
master_reset = 17  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [6, 13, 19,26]  # DIG1, DIG2, DIG3, DIG4

"""conf test
# Nieuwe pinconfiguratie
data_input = 25  # DS
output_enable = 12  # OE (Active LOW)
storage_reg_clck_input = 16  # ST_CP
shift_reg_clck_input = 20  # SH_CP
master_reset = 21  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [5, 6, 13, 19]  # DIG1, DIG2, DIG3, DIG4"""





"""# Configuratie P1
data_input = 25  # DS
output_enable = 12  # OE (Active LOW)
storage_reg_clck_input = 16  # ST_CP
shift_reg_clck_input = 20  # SH_CP
master_reset = 21  # MR (Active LOW)

# Digitale pinnen voor het 7-segment display
digit_pins = [6, 13, 19, 26]  # DIG1, DIG2, DIG3, DIG4"""



"""
configuratie test
DS 23
OE 24
ST_CP 25
SH_CP 12
MR 17




Dit zijn de pinnen voor de digital pinnen van de 7*4 segment : 

DIG1 5
DIG2 6 
DIG3 13
DIG4 19
"""

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
        print(f"Digit {digit}: {digit_value} - Pattern: {bin(pattern)}")  # Debugging output
        write_one_byte(pattern)
        select_digit(digit)
        time.sleep(0.005)  # Delay for persistence of vision

setup()
init_shift_register()

# Lijst van gesimuleerde snelheden in m/s
simulated_speeds_mps = [
    10.23, 0.062, 0.062, 0.062, 0.062, 1.228, 1.709, 2.001,
    1.788, 1.334, 1.095, 0.693, 0.271, 0.301, 0.247, 0.122, 0.068, 0.066,
    0.055, 0.13, 0.038, 0.076, 0.061, 0.083, 0.146, 0.097, 0.09, 0.128,
    0.034, 0.035
]

try:
    while True:
        for speed_mps in simulated_speeds_mps:
            for x in range(50):
                display_speed(speed_mps)
            #time.sleep(1)  # Delay before showing the next speed

except KeyboardInterrupt as e:
    print(e)

finally:
    GPIO.cleanup()

print("Script has stopped!!!")
