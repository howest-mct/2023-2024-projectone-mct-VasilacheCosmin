"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);

let coordinates = [];  // Initialize an empty array to store the route coordinates
let points = [];       // Initialize an empty array to store the points
let totalDistance = 0; // Initialize total distance
let timerInterval;     // To store the timer interval
let startTime; 

const shutdown = function () {
  fetch(`http://${lanIP}/shutdown`, {method: 'POST'})
  .then(response => {
    if (response.ok) {
      alert('Raspberry Pi is shutting down');
    }
    else {
      response.text().then(text => alert(`Shutdown request failed: ${text}`));
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

const startTimer = function() {
    startTime = new Date();

    timerInterval = setInterval(function() {
        let now = new Date();
        let elapsedTime = new Date(now - startTime);
        let hours = String(elapsedTime.getUTCHours()).padStart(2, '0');
        let minutes = String(elapsedTime.getUTCMinutes()).padStart(2, '0');
        let seconds = String(elapsedTime.getUTCSeconds()).padStart(2, '0');
        document.getElementById('timer').textContent = `${hours}:${minutes}:${seconds}`;
    }, 1000);
};

const stopTimer = function() {
    clearInterval(timerInterval);
    document.getElementById('timer').textContent = "00:00:00"; // Reset timer display to 0
};


let map;

const startMeasuring = function() {
  socketio.emit('start_measurement');
  startTimer();
};

const stopMeasuring = function() {
  socketio.emit('stop_measurement');
  stopTimer();
    totalDistance = 0; // Reset total distance
    document.getElementById('distance').textContent = totalDistance.toFixed(2); // Reset distance display to 0
    coordinates = []; // Clear the coordinates array
    points = []; // Clear the points array
};

const listenToUI = function () {
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  const ldrContainer = document.getElementById('ldrContainer');
  const mpuContainer = document.getElementById('mpuContainer');
  const gpsContainer = document.getElementById('gpsContainer');
  const searchButton = document.getElementById('searchButton');
  const mapContainer = document.getElementById('mapContainer');

  if (startButton && stopButton && ldrContainer && mpuContainer && gpsContainer) {
    startButton.addEventListener('click', function() {
      console.log('Startknop ingedrukt');
      startMeasuring();
      ldrContainer.classList.remove('hidden');
      mpuContainer.classList.remove('hidden');
      gpsContainer.classList.remove('hidden');
      mapContainer.classList.remove('hidden');
      totalDistance = 0; // Reset distance at the start of measurement
      document.getElementById('distance').textContent = totalDistance; // Reset distance display
    });

    stopButton.addEventListener('click', function() {
      console.log('Stopknop ingedrukt');
      stopMeasuring();
      ldrContainer.classList.add('hidden');
      mpuContainer.classList.add('hidden');
      gpsContainer.classList.add('hidden');
      mapContainer.classList.remove('hidden');
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

const calculateDistance = function(coord1, coord2) {
  const toRad = function(value) {
    return value * Math.PI / 180;
  };

  const lat1 = coord1[1];
  const lon1 = coord1[0];
  const lat2 = coord2[1];
  const lon2 = coord2[0];

  const R = 6371; // Radius of the Earth in km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c * 1000; // Distance in meters

  return d;
};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('Verbonden met socket webserver');
  });

  socketio.on('B2F_LDR_DATA', function(data) {
    console.log('Data LDR ontvangen', data);
    const ldrElement = document.getElementById('ldr');
    if (ldrElement) {
      ldrElement.innerHTML = data.ldr_value.toFixed(0);
    }
  });

  socketio.on('B2F_MPU6050_DATA', function(data) {
    console.log('Data MPU ontvangen', data);
    const timestampElement = document.getElementById('mpu6050-timestamp');
    const accelTotalElement = document.getElementById('mpu6050-accel-total');

    if (timestampElement && accelTotalElement ) {
      timestampElement.innerHTML = 'Timestamp: ' + data.timestamp;
      accelTotalElement.innerHTML = data.total_accel.toFixed(2);
    }
  });

  socketio.on('B2F_GPS_DATA', function(data) {
    console.log('GPS data ontvangen:', data);
    const latElement = document.getElementById('gps-Lat');
    const lonElement = document.getElementById('gps-long');
    const speedElement = document.getElementById('gps-speed');
    // console.log('Dit zijn de elementen speed - long - lat ')
    // console.log(speedElement)
    // console.log(lonElement)
    // console.log(latElement)

    if (latElement && lonElement && speedElement) {
      latElement.innerHTML = data.lat.toFixed(6);
      lonElement.innerHTML = data.lon.toFixed(6);
      speedElement.innerHTML = data.speed.toFixed(2);
    }

    // Update the route and points on the map
    const newCoord = [data.lon, data.lat];
    coordinates.push(newCoord);

    if (coordinates.length > 1) {
      const lastCoord = coordinates[coordinates.length - 2];
      totalDistance += calculateDistance(lastCoord, newCoord);
      document.getElementById('distance').textContent = totalDistance.toFixed(2); // Update distance display
    }

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
