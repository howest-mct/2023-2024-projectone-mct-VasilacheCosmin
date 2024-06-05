from RPi import GPIO
import time


#ActiveLOW
output_enable =24
#ActiveLOW
master_reset = 17

storage_reg_clck_input = 25
shift_reg_clck_input = 12

data_input = 23


#ds_pin = 23
#oe_pin = 24
#stcp_pin = 25
#shcp_pin = 12
#mr_pin = 17



def setup():
    GPIO.setmode(GPIO.BCM)

    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(data_input, GPIO.OUT)
    GPIO.setup(output_enable, GPIO.OUT)
    GPIO.setup(storage_reg_clck_input, GPIO.OUT)
    GPIO.setup(shift_reg_clck_input, GPIO.OUT)
    GPIO.setup(master_reset, GPIO.OUT)

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
    GPIO.output(data_input,  bitje)
    shift_bits()

def flip_nummer(nummer):
    flipped_nummer = ~nummer & 0xFF
    return flipped_nummer

def write_one_byte(bytetje):
    #eerst flippen om bits in de juiste volgorde terug te krijgen
    byteee =  flip_nummer(bytetje)
    for i in range(8):
        bitjeh = (byteee >> i) &1
        write_one_bit(bitjeh)
        print(f'{bitjeh}')
    print(byteee)
    send_bit()


    





setup()
init_shift_register()
nummerEen = 0b11100000
nummerTwee = 0b11011010
nummerDrie = 0b11110010
nummerVier = 0b01100110
nummerVijf = 0b10110110
nummerZes = 0b10111110
nummerZeven = 0b11100100
nummerAcht = 0b11111110
nummerNegen = 0b11110110
nummerNul = 0b11111110

arrNummers = [nummerNul, nummerEen, nummerTwee, nummerDrie, nummerVier, nummerVijf, nummerZes, nummerZeven, nummerAcht, nummerNegen]
counter = 0

try:
    while True:
        
        for nummer in arrNummers:
            
            time.sleep(0.5)
            write_one_byte(arrNummers[counter])
            print(arrNummers[counter])
            counter += 1
            if counter == 10:
                counter = 0

except KeyboardInterrupt as e:
    print(e)

finally:
    GPIO.cleanup()

print("Script has stopped!!!")