import RPi.GPIO as GPIO
import time
import subprocess
from LCD_klasse import LCD

# Define GPIO mode and setup buttons and joysticks
GPIO.setmode(GPIO.BCM)
knop_display = 18
joystickbtn = 5
GPIO.setup(knop_display, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(joystickbtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Klassen inladen
lcd = LCD()

# Variabelen initialiseren
counter = 0
status = 0
t = 0
prev_time = None
ip_display_last_update = 0
ip_display_state = 0
ip_address_wlan0 = ""

# Functie om alleen het WLAN IP-adres te krijgen
def get_wlan_ip_address():
    ip_a_output = subprocess.check_output(["ip", "a"]).decode("utf-8")
    for line in ip_a_output.split("\n"):
        if "wlan0" in line:
            wlan_index = ip_a_output.split("\n").index(line)
            wlan_ip_line = ip_a_output.split("\n")[wlan_index + 1]
            if "inet " in wlan_ip_line:
                ip_address = wlan_ip_line.split()[1].split("/")[0]
                return ip_address
    return "No WLAN IP"

def display_wlan_ip():
    global ip_address_wlan0
    ip_address_wlan0 = get_wlan_ip_address()
    lcd.clear_display()
    lcd.write_message("IP wlan0:", 1)
    lcd.write_message(ip_address_wlan0, 2)

# Main loop
try:
    last_state = GPIO.input(joystickbtn)
    display_wlan_ip()  # Initial display of the WLAN IP
    while True:
        # Check for joystick button state changes
        current_state = GPIO.input(joystickbtn)
        if current_state != last_state:
            last_state = current_state
            if current_state == False:
                counter += 1
                if counter > 3:
                    counter = 0
                print("Counter:", counter)

        # Update the display every 60 seconds
        current_time = time.time()
        if current_time - ip_display_last_update > 60:
            display_wlan_ip()
            ip_display_last_update = current_time

        time.sleep(0.1)  # Short delay to prevent high CPU usage

except KeyboardInterrupt:
    print("Interrupted by user")
    lcd.clear_display()
    GPIO.cleanup()
