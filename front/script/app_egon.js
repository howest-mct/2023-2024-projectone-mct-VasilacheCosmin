const lanIP = `${window.location.hostname}:5000`;
let socketio;


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
  });

  document.getElementById('stopButton').addEventListener('click', function() {
    console.log('Stopknop ingedrukt');
    stopMeasuring();
  });
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  socketio.on('B2F_TEMPERATURE_DATA', function(data) {
    console.log('Data LDR ontvangen', data);
    if (data.LM35_value !== undefined && !isNaN(data.LM35_value)) {
      document.getElementById('lm35').innerHTML = data.LM35_value.toFixed(2);
    } else {
      console.error("LM35_value is undefined of geen nummer", data.LM35_value);
      document.getElementById('lm35').innerHTML = "N/A";
    }
  });

  socketio.on('measurement_started', function(data) {
    console.log('Measurement started', data);
  });

  socketio.on('measurement_stopped', function(data) {
    console.log('Measurement stopped', data);
    document.getElementById('lm35').innerHTML = "N/A";
  });

  socketio.on('disconnect', function () {
    console.log('Verbinding met socket webserver verbroken');
  });
};

const init = function () {
  console.info('DOM geladen');
  socketio = io(lanIP);
  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);

