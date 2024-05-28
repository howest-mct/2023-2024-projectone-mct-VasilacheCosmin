// frontend.js

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);
// Maak verbinding met de Socket.IO-server


// Update de webpagina met de ontvangen MPU6050-gegevens
socketio.on('B2F_MPU6050_DATA', (data) => {
    document.getElementById('timestamp').innerText = data.timestamp;
    document.getElementById('accel_x').innerText = data.accel_x.toFixed(2);
    document.getElementById('accel_z').innerText = data.accel_z.toFixed(2);
    document.getElementById('speed').innerText = data.speed.toFixed(2);
});

// Log een bericht wanneer de verbinding met de server is gemaakt
socketio.on('connect', () => {
    console.log('Verbonden met de server');
});

// Log een bericht wanneer de verbinding met de server is verbroken
socketio.on('disconnect', () => {
    console.log('Verbinding met de server verbroken');
});

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
};

const init = function () {
  console.info('DOM geladen');
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
