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
        document.getElementById('ldr').innerText = data.ldr_value.toFixed(2);
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