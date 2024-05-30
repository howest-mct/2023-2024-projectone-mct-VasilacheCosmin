import RPi.GPIO as GPIO
import time
import subprocess
#import serial
#import serial.serialutil
from LCD_klasse import LCD


# had het heel graag op deze manier gedaan, maar dit gaf telkens opnieuw een RuntimeError: Failed to add adge detection. Ik heb op meerdere kanalen om feedback gevraagd. (mct discord, oude forums,..)

# GPIO.setup(joystickbtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# def increase_counter(channel):
#     global counter
#     counter += 1
#     if counter > 3:
#         counter = 0


# GPIO.add_event_detect(joystickbtn, GPIO.FALLING, callback=increase_counter, bouncetime=200)

# Define GPIO mode and setup buttons and joysticks
GPIO.setmode(GPIO.BCM)


#klassen inladen
lcd = LCD()


#pin numbers rgb led

counter = 0
status = 0
t = 0
prev_time = None
ip_display_last_update = 0
ip_display_state = 0
ip_addresses = []



def get_ip_addresses():
    ip_addresses = []
    ip_a_output = subprocess.check_output(["ip", "a"]).decode("utf-8")
    for line in ip_a_output.split("\n"):
        if "inet " in line and not "inet6" in line:
            ip_address = line.split()[1].split("/")[0]
            ip_addresses.append(ip_address)
    return ip_addresses

def display_everything():
    global ip_display_last_update, ip_display_state, ip_addresses
   

    if counter == 0:  # IP address display logic
        ip_addresses = get_ip_addresses()           
        lcd.write_message("IP wlan0:", 1)
        lcd.write_message(ip_addresses[2], 2)
            
           


# Main loop
try:
    while True:
        display_everything()
        

except KeyboardInterrupt: #or serial.serialutil.SerialException:
    print("Interrupted by user")
    lcd.clear_display()
    GPIO.cleanup()
