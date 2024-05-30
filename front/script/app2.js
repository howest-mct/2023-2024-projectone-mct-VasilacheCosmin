const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const startMeasuring = function() {
  socketio.emit('start_measurement');
};

const stopMeasuring = function() {
  socketio.emit('stop_measurement');
};

const listenToUI = function () {
  document.getElementById('startButton').addEventListener('click', function() {
    console.log('Startknop ingedrukt');
    startMeasuring();
    document.getElementById('ldrContainer').classList.remove('hidden');
    document.getElementById('mpuContainer').classList.remove('hidden');
    document.getElementById('gpsContainer').classList.remove('hidden');
  });

  document.getElementById('stopButton').addEventListener('click', function() {
    console.log('Stopknop ingedrukt');
    stopMeasuring();
    document.getElementById('ldrContainer').classList.add('hidden');
    document.getElementById('mpuContainer').classList.add('hidden');
    document.getElementById('gpsContainer').classList.add('hidden');
  });
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  socketio.on('B2F_LDR_DATA', function(data) {
    console.log('Data LDR ontvangen', data);
    if (data.ldr_value !== undefined && !isNaN(data.ldr_value)) {
      document.getElementById('ldr').innerHTML = data.ldr_value.toFixed(2);
    } else {
      console.error("LDR_value is undefined of geen nummer", data.ldr_value);
      document.getElementById('ldr').innerHTML = "N/A";
    }
  });

  socketio.on('B2F_MPU6050_DATA', function(data) {
    console.log('Data MPU ontvangen', data);
    document.getElementById('mpu6050-timestamp').innerHTML = 'Timestamp: ' + data.timestamp;
    document.getElementById('mpu6050-accel-x').innerHTML = data.accel_x.toFixed(2);
    document.getElementById('mpu6050-accel-y').innerHTML = data.accel_y.toFixed(2);
    document.getElementById('mpu6050-accel-z').innerHTML = data.accel_z.toFixed(2);
    document.getElementById('mpu6050-speed').innerHTML = data.speed.toFixed(2);
  });

    socketio.on('B2F_GPS_DATA', function(data) {
    console.log('Data GPS ontvangen', data);
    document.getElementById('gps-Lat').innerHTML = data.gps_info['lat'].toFixed(2);
    document.getElementById('gps-long').innerHTML = data.gps_info['lon'].toFixed(2);
    document.getElementById('gps-speed').innerHTML = data.gps_info['speed'].toFixed(2);
  });

//  def read_and_emit_gps_data(gps_client, socketio, stop_event):
//    try:
//        while not stop_event.is_set():
//            data = gps_client.receive_data()
//            if data:
//                gps_info = gps_client.parse_data(data)
//                if gps_info:
//                    print(f"Latitude: {gps_info['lat']}, Longitude: {gps_info['lon']}, Speed: {gps_info['speed']} m/s")
//                    # Save GPS data to DB (assuming a function save_gps_data_to_db is defined)
//                    # save_gps_data_to_db(gps_info['timestamp'], gps_info['lat'], gps_info['lon'], gps_info['speed'])
//                    socketio.emit('B2F_GPS_DATA', gps_info)
//            time.sleep(1)
//    except KeyboardInterrupt:
//        print("GPS data reading stopped")

  socketio.on('measurement_started', function(data) {
    console.log('Measurement started', data);
  });

  socketio.on('measurement_stopped', function(data) {
    console.log('Measurement stopped', data);
    document.getElementById('ldr').innerHTML = "N/A";
  });

  socketio.on('disconnect', function () {
    console.log('Verbinding met socket webserver verbroken');
  });
};

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
