import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, logging, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import smbus
import math
from datetime import date, datetime
import spidev
from MCP3008 import MCP3008
from testSensor import MPU6050
from LCD_klasse import LCD
import subprocess
import RPi.GPIO as GPIO
from gps import GPSClient


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismyveryverysecretkeyformyflask'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)

endpoint = '/api/v1'

reading_thread = None
reading_thread_stop_event = threading.Event()

counter = 0
status = 0
t = 0
prev_time = None
ip_display_last_update = 0
ip_display_state = 0
ip_addresses = []

GPIO.setmode(GPIO.BCM)

# Voor je het backend draait moet je eerst 'cd front/' -> "python3 -m http.server 9000"
# Dit gaat ervoor zorgen dat de frontend draait op poort 9000 ipv 5501 (poort 5501 wilt niet werken for some reason)

def initialize_sensors():
    global mpu, mcp, lcd #, gps_client
    mpu = MPU6050()
    mcp = MCP3008()
    lcd = LCD()
    #gps_client = GPSClient()



def read_and_emit_mpu_data(mpu, socketio, stop_event):
    interval = 1
    vx, vy, vz = 0, 0, 0
    prev_time = time.time()
    mpu.calibrate_mpu6050()

    acceleration_threshold = 0.02

    try:
        while not stop_event.is_set():
            accel_x, accel_y, accel_z = mpu.read_accel_data()
            accel_x -= mpu.offset_x
            accel_y -= mpu.offset_y
            accel_z -= mpu.offset_z

            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time

            vx += accel_x * dt
            vy += accel_y * dt
            vz += accel_z * dt

            if abs(accel_x) < acceleration_threshold:
                vx *= 0.99
            if abs(accel_y) < acceleration_threshold:
                vy *= 0.99
            if abs(accel_z) < acceleration_threshold:
                vz *= 0.99

            instant_speed = math.sqrt(vx**2 + vy**2 + vz**2)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print(f"Versnelling: x={accel_x:.2f}, y={accel_y:.2f}, z={accel_z:.2f}")
            print(f"Ogenblikkelijke snelheid: {instant_speed:.2f} m/s")
            print(f"Timestamp: {timestamp}")

            rit_data = DataRepository.get_ritID()
            print(rit_data[0]['idRit'])
            ritid = rit_data[0]['idRit']

            # Sla de gegevens op in de database
            save_mpu_data_to_db(timestamp, accel_x, accel_y, accel_z, ritid)

            # Emit de gegevens via SocketIO
            socketio.emit('B2F_MPU6050_DATA', {'timestamp': timestamp, 'accel_x': accel_x, 'accel_y': accel_y, 'accel_z': accel_z, 'speed': instant_speed, 'ritid': ritid})
            time.sleep(interval)
    except KeyboardInterrupt:
        print("MPU6050 data reading stopped")

def read_and_emit_ldr_data(mcp, socketio, stop_event):
    try:
        while not stop_event.is_set():
            ldr_value = mcp.read_adc(0)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rit_data = DataRepository.get_ritID()
            print(rit_data[0]['idRit'])
            ritid = rit_data[0]['idRit']
            print(f"LDR waarde: {ldr_value}")
            save_ldr_data_to_db(timestamp, ldr_value, ritid)
            socketio.emit('B2F_LDR_DATA', {'ldr_value': ldr_value , 'idrit' : ritid})
            time.sleep(1)
    except KeyboardInterrupt:
        print("LDR data reading stopped")

"""def read_and_emit_gps_data(gps_client, socketio, stop_event):
    try:
        while not stop_event.is_set():
            data = gps_client.receive_data()
            if data:
                gps_info = gps_client.parse_data(data)
                if gps_info:
                    print(f"Latitude: {gps_info['lat']}, Longitude: {gps_info['lon']}, Speed: {gps_info['speed']} m/s")
                    # Save GPS data to DB (assuming a function save_gps_data_to_db is defined)
                    # save_gps_data_to_db(gps_info['timestamp'], gps_info['lat'], gps_info['lon'], gps_info['speed'])
                    socketio.emit('B2F_GPS_DATA', gps_info)
            time.sleep(1)
    except KeyboardInterrupt:
        print("GPS data reading stopped")"""



def get_ip_addresses():
    ip_addresses = []
    ip_a_output = subprocess.check_output(["ip", "a"]).decode("utf-8")
    for line in ip_a_output.split("\n"):
        if "inet " in line and not "inet6" in line:
            ip_address = line.split()[1].split("/")[0]
            ip_addresses.append(ip_address)
    return ip_addresses

def display_ip():
    while True:
        ip_addresses = get_ip_addresses()
        if len(ip_addresses) > 2:
            ip_address = ip_addresses[2]
        else:
            ip_address = "No WLAN IP"
        if len(ip_address) > 16:
            ip_address = ip_address[:16]  # Zorg ervoor dat het IP-adres niet langer is dan 16 tekens
        lcd.write_message("IP wlan0:", 1)
        lcd.write_message(ip_address, 2)
        time.sleep(10)  # Update every 10 seconds

# Functie om MPU6050 gegevens op te slaan in de database
def save_mpu_data_to_db(timestamp, accel_x, accel_y, accel_z,ritid):
    DataRepository.save_mpu_data(timestamp, accel_x, accel_y, accel_z,ritid)

# Functie om LDR gegevens op te slaan in de database
def save_ldr_data_to_db(timestamp, ldr_value, ritid):
    DataRepository.save_ldr_data(timestamp, ldr_value, ritid)

# Webserver en SocketIO
@app.route('/')
def hallo():
    return render_template('index.html')


@app.route('/index2.html')
def index2():
    return render_template('index2.html')



@app.route(f'{endpoint}/licht/<int:rit_id>/', methods=['GET'])
def get_licht_by_rit_id(rit_id):
    if request.method == 'GET':
        data = DataRepository.read_lichtintensiteit_by_rit_id(rit_id)
        if data:
            return jsonify(bestemmingen=data), 200
        else:
            return jsonify({"error": "Data not found"}), 404
        

@app.route(f'{endpoint}/licht/gemiddelde/', methods=['GET'])
def get_gemiddelde_licht_per_rit():
    try:
        data = DataRepository.read_alles_lichtintensiteit_byID()
        #print(f"Data received: {data}")
        if data:
            # Bereken gemiddelde per ritID
            rit_data = {}
            for item in data:
                rit_id = item['RitID']
                meting = item['Meting']
                timestamp = item['InleesTijd']
                if rit_id not in rit_data:
                    rit_data[rit_id] = {'metingen': [], 'timestamps': []}
                rit_data[rit_id]['metingen'].append(meting)
                rit_data[rit_id]['timestamps'].append(timestamp)
            
            gemiddelde_data = []
            for rit_id, waarden in rit_data.items():
                gemiddelde = sum(waarden['metingen']) / len(waarden['metingen'])
                eerste_timestamp = waarden['timestamps'][0]  # Gebruik de eerste timestamp
                gemiddelde_data.append({
                    'rit_id': rit_id,
                    'gemiddelde': gemiddelde,
                    'first_timestamp': eerste_timestamp
                })
            
            #print(f"Calculated averages: {gemiddelde_data}")
            return jsonify(bestemmingen=gemiddelde_data), 200
        else:
            print("No data found")
            return jsonify({"error": "Data not found"}), 404
    except Exception as e:
        print("Exception occurred while processing the request")
        return jsonify({"error": str(e)}), 500
    


@app.route(f'{endpoint}/licht/today/', methods=['GET'])
def get_today_licht():
    try:
        # Huidige datum
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        data = DataRepository.read_lichtintensiteit_TODAY(today_start, today_end)
        #print(f"Data received for today: {data}")

        if data:
            return jsonify(bestemmingen=data), 200
        else:
            print("No data found for today")
            return jsonify({"error": "Data not found"}), 404
    except Exception as e:
        print("Exception occurred while processing the request")
        return jsonify({"error": str(e)}), 500

    

@app.route(endpoint + '/licht/', methods=['GET'])
def get_licht():
    if request.method == 'GET':
        return jsonify(bestemmingen=DataRepository.read_alles_lichtintensiteit()), 200
    # het is niet nodig om de andere methods te voorzien.

@app.route(endpoint + '/licht/id/', methods=['GET'])
def read_alles_lichtintensiteit_byID():
    if request.method == 'GET':
        return jsonify(bestemmingen=DataRepository.read_alles_lichtintensiteit_byID()), 200
    # het is niet nodig om de andere methods te voorzien.

@socketio.on('connect')
def initial_connection(auth):
    print('A new client connected')

@socketio.on('start_measurement')
def handle_start_measurement():
    global reading_thread, reading_thread_stop_event, mpu, mcp
    if reading_thread is None or not reading_thread.is_alive():
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_session(start_time)
        reading_thread_stop_event.clear()

        reading_thread = threading.Thread(target=read_and_emit_ldr_data, args=(mcp, socketio, reading_thread_stop_event), daemon=True)
        reading_thread.start()

        #reading_thread = threading.Thread(target=read_and_emit_gps_data, args=(gps_client, socketio, reading_thread_stop_event), daemon=True)
        #reading_thread.start()
        
        # Start MPU6050 in een aparte thread
        threading.Thread(target=read_and_emit_mpu_data, args=(mpu, socketio, reading_thread_stop_event), daemon=True).start()
        
        print('Measurement started')
        print(start_time)
        emit('measurement_started', {'status': 'started'})
        

@socketio.on('stop_measurement')
def handle_stop_measurement():
    global reading_thread_stop_event
    if reading_thread and reading_thread.is_alive():
        reading_thread_stop_event.set()
        reading_thread.join()
        print('Measurement stopped')
        emit('measurement_stopped', {'status': 'stopped'})
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_session(end_time)

def save_session(timestamp):
    DataRepository.save_session(timestamp)

def end_session(timestamp):
    DataRepository.end_session(timestamp)

def webserver():
    print("Webserver started")
    socketio.run(app, debug=False, host='0.0.0.0')

if __name__ == '__main__':
    try:
        print("**** Starting APP ****")
        initialize_sensors()
        threading.Thread(target=display_ip, daemon=True).start()  # Start LCD IP display thread
        webserver()
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("Finished")
