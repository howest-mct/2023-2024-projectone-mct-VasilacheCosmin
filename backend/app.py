import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import smbus
import math
from datetime import datetime
import spidev
from MCP3008 import MCP3008
from testSensor import MPU6050

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismyveryverysecretkeyformyflask'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)



# MPU6050 data uitlezen en versturen
#def read_and_emit_mpu_data(mpu, socketio):
#    interval = 0.1
#    vx, vz = 0, 0
#    prev_time = time.time()
#    mpu.calibrate_mpu6050()
#
#    acceleration_threshold = 0.02
#
#    try:
#        while True:
#            accel_x, accel_z = mpu.read_accel_data()
#            accel_x -= mpu.offset_x
#            accel_z -= mpu.offset_z
#
#            current_time = time.time()
#            dt = current_time - prev_time
#            prev_time = current_time
#
#            vx += accel_x * dt
#            vz += accel_z * dt
#
#            if abs(accel_x) < acceleration_threshold:
#                vx *= 0.99
#            if abs(accel_z) < acceleration_threshold:
#                vz *= 0.99
#
#            instant_speed = math.sqrt(vx**2 + vz**2)
#            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#            print(f"Versnelling: x={accel_x:.2f}, z={accel_z:.2f}")
#            print(f"Ogenblikkelijke snelheid: {instant_speed:.2f} m/s")
#            print(f"Timestamp: {timestamp}")
#
#            socketio.emit('B2F_MPU6050_DATA', {'timestamp': timestamp, 'accel_x': accel_x, 'accel_z': accel_z, 'speed': instant_speed})
#            time.sleep(interval)
#    except KeyboardInterrupt:
#        print("MPU6050 data reading stopped")
#
# LDR uitlezen en data versturen
def read_and_emit_ldr_data(mcp, socketio):
    try:
        while True:
            ldr_value = mcp.read_adc(0)
            print(f"LDR waarde: {ldr_value}")
            socketio.emit('B2F_LDR_DATA', {'ldr_value': ldr_value})
            time.sleep(1)
    except KeyboardInterrupt:
        print("LDR data reading stopped")

# Webserver en SocketIO
@app.route('/')
def hallo():
    return render_template('index.html')

#@socketio.on('connect')
#def initial_connection(auth):
#    print('A new client connected')
#    emit('B2F_status_lampen', {'lampen': DataRepository.read_status_lampen()}, broadcast=False)
#    # Emit initial LDR and MPU data
#    ldr_value = mcp.read_adc(0)
#    emit('B2F_LDR_DATA', {'ldr_value': ldr_value})
#    mpu_data = mpu.read_accel_data()
#    emit('B2F_MPU6050_DATA', {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'accel_x': mpu_data[0], 'accel_z': mpu_data[1], 'speed': 0})

@socketio.on('connect')
def initial_connection(auth):
    print('A new client connected')

def webserver():
    print("webserver started")
    socketio.run(app, debug=False, host='0.0.0.0')

def start_thread():
    #threading.Thread(target=webserver, daemon=True).start()
    # Start MPU6050 in een aparte thread
    #global mpu
    #mpu = MPU6050()
    #threading.Thread(target=read_and_emit_mpu_data, args=(mpu, socketio), daemon=True).start()
    # Start MCP3008 (LDR) in een aparte thread
    global mcp
    mcp = MCP3008()
    threading.Thread(target=read_and_emit_ldr_data, args=(mcp, socketio), daemon=True).start()

if __name__ == '__main__':
    try:
        print("**** Starting APP ****")
        start_thread()
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("finished")
