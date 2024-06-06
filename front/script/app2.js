"use strict"

const lanIP = `${window.location.hostname}:5000`;
console.log(lanIP);
const socketio = io(lanIP);

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
//
//const fetchData = async (url) => {
//  const response = await fetch(url);
//  const data = await response.json();
//  return data.bestemmingen;
//};
////
//const createChart = (elementId, data, title, labels) => {
//  const options = {
//    series: [{
//      name: title,
//      data: data
//    }],
//    chart: {
//      type: 'area',
//      height: 350,
//      zoom: {
//        enabled: false
//      }
//    },
//    dataLabels: {
//      enabled: false
//    },
//    stroke: {
//      curve: 'straight'
//    },
//    title: {
//      text: title,
//      align: 'left'
//    },
//    subtitle: {
//      text: 'Price Movements',
//      align: 'left'
//    },
//    labels: labels,
//    xaxis: {
//      type: 'datetime',
//    },
//    yaxis: {
//      min: 0,
//      max: 1024,
//      opposite: true
//    },
//    legend: {
//      horizontalAlign: 'left'
//    }
//  };
//
//  const chart = new ApexCharts(document.querySelector(elementId), options);
//  chart.render();
//};
//
//const initCharts = async (ritId) => {
//  const data = await fetchData(`http://${lanIP}/api/v1/licht/${ritId}/`);
//  createChart('#chart1', data.map(item => item.Meting), 'Lichtintensiteit', data.map(item => item.InleesTijd));
//};
//
//const initAverageChart = async () => {
//  const data = await fetchData(`http://${lanIP}/api/v1/licht/gemiddelde/`);
//  createChart('#chart2', data.map(item => item.gemiddelde), 'Gemiddelde licht per rit', data.map(item => item.first_timestamp));
//}
//
//
//
//const loadTodayData = async () => {
//  const data = await fetchData(`http://${lanIP}/api/v1/licht/today/`);
//  console.log('Data for today:', data); // Log de data om te controleren of deze correct is
//
//  const chartContainer = document.getElementById('chartContainer');
//  chartContainer.innerHTML = ''; // Clear previous charts
//
//  // Groepeer de data op rit_id
//  const groupedData = data.reduce((acc, item) => {
//    if (!acc[item.rit_id]) {
//      acc[item.rit_id] = [];
//    }
//    acc[item.rit_id].push(item);
//    return acc;
//  }, {});
//
//  // Maak een grafiek voor elke rit
//  Object.keys(groupedData).forEach((ritId, index) => {
//    const chartData = groupedData[ritId].map(item => item.meting);
//    const chartLabels = groupedData[ritId].map(item => item.InleesTijd);
//    const chartId = `chart${index}`;
//    const chartDiv = document.createElement('div');
//    chartDiv.id = chartId;
//    chartContainer.appendChild(chartDiv);
//
//    createChart(`#${chartId}`, chartData, `Rit ${ritId}`, chartLabels);
//  });
//};
//
const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
  //initAverageChart();
};

document.addEventListener('DOMContentLoaded', init);
