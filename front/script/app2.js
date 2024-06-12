"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let coordinates = [];  // Initialize an empty array to store the route coordinates
let points = [];       // Initialize an empty array to store the points


const shutdown = function () {
  fetch(`http://${lanIP}/shutdown`, {method: 'POST'})
  .then(response => {
    if (response.ok) {
      alert('Raspberry Pi is shutting down');
    }
    else {
      response.text().then(text => alert(`Shutdown request failed: ${error}`));
    }
  })
  .catch(error => alert(`Shutdown request failed: ${error}`));
}

const initMap = function() {
  mapboxgl.accessToken = 'pk.eyJ1IjoiYXJ0aHVybWV5ZnJvaWR0IiwiYSI6ImNsdWJ4eGE5dTBhanUyanAzaTB4ZHN2cW0ifQ.NrOlYkV5MHPVQfUxq8NjjQ';
  const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [3.250204343433751, 50.82413300539262],
      zoom: 15
  });

  map.on('load', function () {
      map.addSource('route', {
          'type': 'geojson',
          'data': {
              "type": "Feature",
              "geometry": {
                  "type": "LineString",
                  "coordinates": coordinates
              }
          }
      });

      map.addLayer({
          'id': 'route',
          'type': 'line',
          'source': 'route',
          'paint': {
              'line-color': '#888',
              'line-width': 5
          }
      });

      map.addSource('points', {
          'type': 'geojson',
          'data': {
              "type": "FeatureCollection",
              "features": points
          }
      });

      map.addLayer({
          'id': 'points',
          'type': 'circle',
          'source': 'points',
          'paint': {
              'circle-radius': 6,
              'circle-color': '#B42222'
          }
      });

      console.log('Map loaded and route source added');
  });

  return map;
};

let map;

const startMeasuring = function() {
  socketio.emit('start_measurement');
};

const stopMeasuring = function() {
  socketio.emit('stop_measurement');
};

const listenToUI = function () {
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  const ldrContainer = document.getElementById('ldrContainer');
  const mpuContainer = document.getElementById('mpuContainer');
  const gpsContainer = document.getElementById('gpsContainer');
  const searchButton = document.getElementById('searchButton');
  // const todayButton = document.getElementById('todayButton');

  if (startButton && stopButton && ldrContainer && mpuContainer && gpsContainer) {
    startButton.addEventListener('click', function() {
      console.log('Startknop ingedrukt');
      startMeasuring();
      ldrContainer.classList.remove('hidden');
      mpuContainer.classList.remove('hidden');
      gpsContainer.classList.remove('hidden');
      // todayButton.addEventListener('click', function() {
      // loadTodayData();
    // });
      
    });

    stopButton.addEventListener('click', function() {
      console.log('Stopknop ingedrukt');
      stopMeasuring();
      ldrContainer.classList.add('hidden');
      mpuContainer.classList.add('hidden');
      gpsContainer.classList.add('hidden');
    });
  }

  if (searchButton) {
    searchButton.addEventListener('click', function() {
      const ritId = document.getElementById('ritIdInput').value;
      if (ritId) {
        initCharts(ritId);
      }
    });
  }
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  socketio.on('B2F_LDR_DATA', function(data) {
    console.log('Data LDR ontvangen', data);
    const ldrElement = document.getElementById('ldr');
    if (ldrElement) {
      ldrElement.innerHTML = data.ldr_value.toFixed(2);
    }
  });

  
  socketio.on('measurement_started', function(data) {
    console.log("Started")
  });

  socketio.on('B2F_MPU6050_DATA', function(data) {
    console.log('Data MPU ontvangen', data);
    const timestampElement = document.getElementById('mpu6050-timestamp');
    const accelXElement = document.getElementById('mpu6050-accel-x');
    const accelYElement = document.getElementById('mpu6050-accel-y');
    const accelZElement = document.getElementById('mpu6050-accel-z');
    const speedElement = document.getElementById('mpu6050-speed');

    if (timestampElement && accelXElement && accelYElement && accelZElement && speedElement) {
      timestampElement.innerHTML = 'Timestamp: ' + data.timestamp;
      accelXElement.innerHTML = data.accel_x.toFixed(2);
      accelYElement.innerHTML = data.accel_y.toFixed(2);
      accelZElement.innerHTML = data.accel_z.toFixed(2);
      speedElement.innerHTML = data.speed.toFixed(2);
    }
  });

  socketio.on('B2F_GPS_DATA', function(data) {
    console.log('GPS data ontvangen:', data);
    const latElement = document.getElementById('gps-Lat');
    const lonElement = document.getElementById('gps-long');
    const speedElement = document.getElementById('gps-speed');

    if (latElement && lonElement && speedElement) {
      latElement.innerHTML = parseFloat(data.lat).toFixed(6);
      lonElement.innerHTML = parseFloat(data.lon).toFixed(6);
      speedElement.innerHTML = parseFloat(data.speed).toFixed(2);
    }

    // Update the route and points on the map
    const newCoord = [data.lon, data.lat];
    coordinates.push(newCoord);

    points.push({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": newCoord
        }
    });

    if (map.getSource('route')) {
      console.log('Updating route on map with coordinates', coordinates);
      map.getSource('route').setData({
        "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": coordinates
        }
      });
    } else {
      console.log('Route source not found on map');
    }

    if (map.getSource('points')) {
      console.log('Updating points on map with coordinates', points);
      map.getSource('points').setData({
        "type": "FeatureCollection",
        "features": points
      });
    } else {
      console.log('Points source not found on map');
    }

    // Center the map on the new location
    map.setCenter(newCoord);
  });

  socketio.on('measurement_started', function(data) {
    console.log('Measurement started', data);
  });

  socketio.on('measurement_stopped', function(data) {
    console.log('Measurement stopped', data);
    const ldrElement = document.getElementById('ldr');
    if (ldrElement) {
      ldrElement.innerHTML = "N/A";
    }
  });

  socketio.on('disconnect', function () {
    console.log('Verbinding met socket webserver verbroken');
  });
};

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
  map = initMap(); // Initialize the map
};

document.addEventListener('DOMContentLoaded', init);
