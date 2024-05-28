import RPi.GPIO as GPIO
import time

# Gebruik Broadcom SOC pin numbering schema
GPIO.setmode(GPIO.BCM)

# Definieer de pin die je wilt testen
test_pin = 13 # Bijvoorbeeld4 GPIO 18


# pin 4 stond half aan na testen van pin 18, 
# na test van pin 17 , staan pinnen x half aan : 18,5,6
# ik denk dat 18,5,6 verbrand zijn

# test lukte wel op 18,5,6 en na de test deden de pinnen niet meer raar



# Stel de pin in als uitgang
GPIO.setup(test_pin, GPIO.OUT)

try:
    while True:
        # Zet de pin hoog
        GPIO.output(test_pin, GPIO.HIGH)
        print(f"Pin {test_pin} is HIGH")
        time.sleep(5)  # Wacht 5 seconden

        # Zet de pin laag
        GPIO.output(test_pin, GPIO.LOW)
        print(f"Pin {test_pin} is LOW")
        time.sleep(5)  # Wacht 5 seconden

except KeyboardInterrupt:
    # Clean up de GPIO settings voordat je het programma afsluit
    GPIO.cleanup()
    print("\nGPIO cleaned up and program exited")
