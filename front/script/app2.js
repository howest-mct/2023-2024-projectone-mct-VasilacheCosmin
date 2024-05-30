const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const listenToUI = function () { 
  // Event listeners for UI interactions can be added here
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  socketio.on('B2F_LDR_DATA', function(data) {
        console.log('Data LDR ontvangen', data)
        document.getElementById('ldr').innerHTML = data.ldr_value.toFixed(2);
    });

        socketio.on('B2F_MPU6050_DATA', function(data) {
        console.log('Data MPU ontvangen', data)
        document.getElementById('mpu6050-timestamp').innerHTML = 'Timestamp: ' + data.timestamp;
        document.getElementById('mpu6050-accel-x').innerHTML = data.accel_x.toFixed(2);
        document.getElementById('mpu6050-accel-y').innerHTML = data.accel_y.toFixed(2);
        document.getElementById('mpu6050-accel-z').innerHTML = data.accel_z.toFixed(2);
        document.getElementById('mpu6050-speed').innerHTML = data.speed.toFixed(2);
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