import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# TODO: GPIO
import smbus2
import time
import numpy as np
from collections import deque
from scipy.signal import butter, filtfilt, find_peaks
from testingcomponents.max30102 import MAX30102
from testingcomponents.airquality import MCP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismyveryverysecretkeyformyflask'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def all_out():
    # wait 10s with sleep sintead of threading.Timer, so we can use daemon
    time.sleep(10)
    while True:
        print('*** We zetten alles uit **')
        DataRepository.update_status_alle_lampen(0)
        status = DataRepository.read_status_lampen()
        socketio.emit('B2F_alles_uit', {
                    'status': "lampen uit"})
        socketio.emit('B2F_status_lampen', {'lampen': status})
        # save our last run time
        last_time_alles_uit = time.time()
        time.sleep(30)

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."



# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_status_lampen()
    # socketio.emit('B2F_status_lampen', {'lampen': status})
    # Beter is het om enkel naar de client te sturen die de verbinding heeft gemaakt.
    emit('B2F_status_lampen', {'lampen': status}, broadcast=False)


@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit', data)
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    # spreek de hardware aan
    # stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)
    print(res)
    # vraag de (nieuwe) status op van de lamp
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp',  {'lamp': data})
    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    if lamp_id == '3':
        print(f"TV kamer moet switchen naar {new_status} !")
        # Do something

#ALL RASPBERRYPI PHYSICAL CODE

#FOR MAX30102:


def Max30102():
    fs = 100  # Sampling frequency (Hz)
    max_sensor = MAX30102()
    ir_data_deque = deque(maxlen=1000)  # Store enough data for analysis

    while True:
        ir_data, red_data = max_sensor.read_fifo()
        if ir_data:
            ir_data_deque.extend(ir_data)

            # Calculate BPM every second
            if len(ir_data_deque) >= 100:
                filtered_ir = max_sensor.bandpass_filter(list(ir_data_deque), lowcut=0.5, highcut=5.0, fs=fs, order=3)
                peaks, _ = find_peaks(filtered_ir, distance=fs/3)  # minimum 1/3 seconde per peak?
                bpm_values = max_sensor.calculate_bpm(peaks, fs=fs)
                if len(bpm_values) > 0:
                    average_bpm = np.mean(bpm_values)
                    # print(f"Average BPM: {average_bpm:.2f}")
                    temp = average_bpm.round(2)
                    socketio.emit('B2F_AVERAGE_BPM', {'AVERAGE_BPM': temp}) 
        time.sleep(0.5)


def read_temperature():
    directory_path = "/sys/bus/w1/devices/28-00000de601b0/w1_slave"
    while True:
        with open(directory_path, "r") as file:
            content = file.read()
            temp_string = content.split("t=")[1]
            temp = int(temp_string) / 1000
            socketio.emit('B2F_TEMPERATURE', {'temperature': temp})
        time.sleep(0.5)

def read_airquality():
    mcp = MCP()
    channel = 0
    while True:
        data = mcp.read_channel(channel)
        voltage = mcp.convert_to_voltage(data)
        # print(f"Channel {channel} \n voltage: {voltage}V \n data: {data} ")
        socketio.emit('B2F_QUALITY', {'quality': data})
        time.sleep(0.5)



def webserver():
    print("webserver started")
    socketio.run(app, debug=False, host='0.0.0.0')

def start_thread():
    # threading.Timer(10, all_out).start()
    threading.Thread(target=webserver, daemon=True).start()
    threading.Thread(target=Max30102, daemon=True).start()
    threading.Thread(target=read_temperature, daemon=True).start()
    threading.Thread(target=read_airquality, daemon=True).start()
    print("threads started")


if __name__ == '__main__':
    try:
        print("**** Starting APP ****")
        start_thread()
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("finished")





