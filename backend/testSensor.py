 #MPU6050 Klasse
#from datetime import datetime
import smbus
import time


class MPU6050:
    MPU6050_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F

    def __init__(self, bus_num=1):
        self.bus = smbus.SMBus(bus_num)
        self.bus.write_byte_data(self.MPU6050_ADDR, self.PWR_MGMT_1, 0)
        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0

    def read_word_2c(self, addr):
        high = self.bus.read_byte_data(self.MPU6050_ADDR, addr)
        low = self.bus.read_byte_data(self.MPU6050_ADDR, addr + 1)
        val = (high << 8) + low
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def read_accel_data(self):
        accel_x = self.read_word_2c(self.ACCEL_XOUT_H)
        accel_y = self.read_word_2c(self.ACCEL_YOUT_H)
        accel_z = self.read_word_2c(self.ACCEL_ZOUT_H)
        
        accel_x /= 16384.0
        accel_y /= 16384.0
        accel_z /= 16384.0
        
        return accel_x, accel_y, accel_z

    def calibrate_mpu6050(self, samples=1000):
        print("Kalibreren... Houd de sensor stil.")
        offset_x, offset_y, offset_z = 0, 0, 0
        
        for _ in range(samples):
            accel_x, accel_y, accel_z = self.read_accel_data()
            offset_x += accel_x
            offset_y += accel_y
            offset_z += accel_z
            time.sleep(0.001)
        
        self.offset_x = offset_x / samples
        self.offset_y = offset_y / samples
        self.offset_z = offset_z / samples
        
        print(f"Kalibratie voltooid. Offsets: x={self.offset_x}, y={self.offset_y}, z={self.offset_z}")