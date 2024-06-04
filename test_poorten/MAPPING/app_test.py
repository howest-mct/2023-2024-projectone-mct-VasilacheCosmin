
import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import smbus
import math
#import numpy as np
#from collections import deque
#from scipy.signal import butter, filtfilt, find_peaks
#
#from classes.mpu6050 import PunchSpeedSensor
#from classes.FSR import ForceSensitiveResistor
#from classes.heart import MAX30102
#
## Initialize the sensor
#sensor = PunchSpeedSensor()
#power = ForceSensitiveResistor()
#heart = MAX30102()

# Flask application setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSECRET'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)

# Function to read sensor data and emit it via Socket.IO
def read_sensor_data():
    while True:
        max_velocity_kmh, duration = sensor.measure_punch_speed()
        force_newtons = power.read_force()
        if max_velocity_kmh > 0:
            socketio.emit('B2F_punch_speed', {'speed': max_velocity_kmh, 'duration': duration, 'force': force_newtons})
        time.sleep(1)  # adjust the sleep time as necessary

# Function to start the sensor thread
def start_sensor_thread():
    t = threading.Thread(target=read_sensor_data, daemon=True)
    t.start()
    print("Sensor thread started")

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# SOCKET IO EVENTS
@socketio.on('connect')
def initial_connection():
    print('A new client connected')



if __name__ == '__main__':
    try:
        start_sensor_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Finished")
