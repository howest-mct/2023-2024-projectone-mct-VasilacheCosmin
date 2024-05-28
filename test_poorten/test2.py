import smbus
import time
import math
import mysql.connector
from datetime import datetime

# MPU6050 registers and addresses
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_ZOUT_H = 0x3F

bus = smbus.SMBus(1)  # SMBus(1) voor Raspberry Pi 2 en later

# Initialiseer de MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_word_2c(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def read_accel_data():
    accel_x = read_word_2c(ACCEL_XOUT_H)
    accel_z = read_word_2c(ACCEL_ZOUT_H)
    
    accel_x /= 16384.0
    accel_z /= 16384.0
    
    return accel_x, accel_z

def calibrate_mpu6050(samples=1000):
    print("Kalibreren... Houd de sensor stil.")
    offset_x, offset_z = 0, 0
    
    for _ in range(samples):
        accel_x, accel_z = read_accel_data()
        offset_x += accel_x
        offset_z += accel_z
        time.sleep(0.001)  # kleine pauze tussen metingen
    
    offset_x /= samples
    offset_z /= samples
    
    print(f"Kalibratie voltooid. Offsets: x={offset_x}, z={offset_z}")
    return offset_x, offset_z

def store_data(timestamp, accel_x, accel_z, speed):
    conn = mysql.connector.connect(
        host="user@192.168.168.169",
        user="dbuser",
        password="P@ssw0rd",
        database="Project1_DB"
    )
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO VersnellingsS (InleesTijd, Meting, meting_Y, snelheid) 
    VALUES (%s, %s, %s, %s)
    ''', (timestamp, accel_x, accel_z, speed))
    
    conn.commit()
    cursor.close()
    conn.close()

def main():
    interval = 0.1  # tijdinterval in seconden
    vx, vz = 0, 0  # initialiseer snelheid
    prev_time = time.time()

    # Kalibreer de MPU6050
    offset_x, offset_z = calibrate_mpu6050()

    # Drempel voor reset
    acceleration_threshold = 0.02  # Drempelwaarde om te bepalen wanneer de sensor stil is

    try:
        while True:
            accel_x, accel_z = read_accel_data()
            
            # Pas offsets toe om versnellingswaarden te corrigeren
            accel_x -= offset_x
            accel_z -= offset_z

            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time

            # Bereken de snelheden door integratie
            vx += accel_x * dt
            vz += accel_z * dt

            # Controleer de versnelling en pas snelheid aan
            if abs(accel_x) < acceleration_threshold:
                vx *= 0.99  # Verlaag de snelheid als versnelling bijna 0 is
            if abs(accel_z) < acceleration_threshold:
                vz *= 0.99

            # Bereken de ogenblikkelijke snelheid
            instant_speed = math.sqrt(vx**2 + vz**2)

            # Verkrijg de huidige datum en tijd
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print(f"Versnelling: x={accel_x:.2f}, z={accel_z:.2f}")
            print(f"Ogenblikkelijke snelheid: {instant_speed:.2f} m/s")
            print(f"Timestamp: {timestamp}")

            # Sla de gegevens op in de database
            store_data(timestamp, accel_x, accel_z, instant_speed)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("Programma gestopt")

if __name__ == "__main__":
    main()