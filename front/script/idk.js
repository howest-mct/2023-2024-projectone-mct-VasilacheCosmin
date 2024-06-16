 "use strict";

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

let sessionid = 0;
let chartLDR, chartVersnelling , chartSnelheid;
let sessionidhtml;

let ldrData, versnellingsData, snelheidData = [];
let chartTime,chartTime2, chartTime3 = [];

// Initialize the map and set global variables for routes and points
const initMap = function () {
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
          "coordinates": []
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
        "features": []
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

  window.map = map;
};

const showChartsLDR = function (data, time) {
    ldrData = data;
    chartTime = time;

    if (chartLDR) {
        chartLDR.destroy();
    }

    let options = {
        series: [
            {
                name: 'LDR',
                data: data,
            },
        ],
        chart: {
            height: 200,
            type: 'line',
            zoom: {
                enabled: false,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: 'straight',
            colors: ['#008FFB'], // Blue line
        },
        title: {
            text: 'LDR',
            align: 'left',
            style: {
                color: '#000000' // Black text for the title
            }
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5,
            },
        },
        xaxis: {
            categories: time,
            labels: {
                show: false,
            },
        },
        tooltip: {
            theme: 'light', // Light theme for tooltip
            style: {
                fontSize: '12px',
                fontFamily: undefined,
                background: '#FFFFFF',
                color: '#000000' // Black text in tooltip
            },
            marker: {
                show: true,
            },
            x: {
                show: true,
                format: 'HH:mm:ss',
                formatter: undefined,
            },
            y: {
                title: {
                    formatter: seriesName => seriesName,
                },
            },
        },
        yaxis: {
            labels: {
                style: {
                    colors: ['#000000'], // Black text for y-axis labels
                },
            },
        },
    };

    chartLDR = new ApexCharts(document.querySelector('.js-chartbpmsession'), options);
    chartLDR.render();
};


const showChartsSnelheid = function (data, time) {
    let snelheidData = data;
    let chartTime3 = time;

    if (chartSnelheid) {
        chartSnelheid.destroy();
    }

    let options = {
        series: [
            {
                name: 'Snelheid',
                data: snelheidData,
            },
        ],
        chart: {
            height: 200,
            type: 'line',
            zoom: {
                enabled: false,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: 'straight',
            colors: ['#008FFB'], // Blue line
        },
        title: {
            text: 'Snelheid',  // Corrected title
            align: 'left',
            style: {
                color: '#000000' // Black text for the title
            }
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5,
            },
        },
        xaxis: {
            categories: chartTime3,
            labels: {
                show: true,
            },
        },
        tooltip: {
            theme: 'light', // Light theme for tooltip
            style: {
                fontSize: '12px',
                fontFamily: undefined,
                background: '#FFFFFF',
                color: '#000000' // Black text in tooltip
            },
            marker: {
                show: true,
            },
            x: {
                show: true,
                format: 'HH:mm:ss',
                formatter: undefined,
            },
            y: {
                title: {
                    formatter: seriesName => seriesName,
                },
            },
        },
        yaxis: {
            labels: {
                style: {
                    colors: ['#000000'], // Black text for y-axis labels
                },
            },
        },
    };

    chartSnelheid = new ApexCharts(document.querySelector('.js-chartSnelheidsession'), options);
    chartSnelheid.render();
};



const showChartsVersnelling = function (data, time) {
    versnellingsData = data;
    chartTime2 = time;

    if (chartVersnelling) {
        chartVersnelling.destroy();
    }

    let options = {
        series: [
            {
                name: 'Versnelling',
                data: data,
            },
        ],
        chart: {
            height: 200,
            type: 'line',
            zoom: {
                enabled: false,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: 'straight',
            colors: ['#008FFB'], // Blue line
        },
        title: {
            text: 'Versnelling',
            align: 'left',
            style: {
                color: '#000000' // Black text for the title
            }
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5,
            },
        },
        xaxis: {
            categories: time,
            labels: {
                show: false,
            },
        },
        tooltip: {
            theme: 'light', // Light theme for tooltip
            style: {
                fontSize: '12px',
                fontFamily: undefined,
                background: '#FFFFFF',
                color: '#000000' // Black text in tooltip
            },
            marker: {
                show: true,
            },
            x: {
                show: true,
                format: 'HH:mm:ss',
                formatter: undefined,
            },
            y: {
                title: {
                    formatter: seriesName => seriesName,
                },
            },
        },
        yaxis: {
            labels: {
                style: {
                    colors: ['#000000'], // Black text for y-axis labels
                },
            },
        },
    };

    chartVersnelling = new ApexCharts(document.querySelector('.js-chartVersnellingSession'), options);
    chartVersnelling.render();
};

const fetchLDR = function (data) {
    console.log("Ontvangen data:", data);
    console.log('dit is .bestemmingen', data.bestemmingen);

    let values = [];
    let times = [];

    for (let i = 0; i < data.bestemmingen.length; i++) {
        let item = data.bestemmingen[i];
        values.push(item.Meting);
        times.push(new Date(item.InleesTijd).toLocaleTimeString());
    }

    showChartsLDR(values, times);
};

const showSessionID = function (data) {
    console.log(data);

    for (let i = 0; i < data.bestemmingen.length; i++) {
        
        sessionidhtml = document.querySelector('.js-sessionid');

        let str = `
            <option value="${data.bestemmingen[i].RitID}">${data.bestemmingen[i].RitID}</option>
        `;

        sessionidhtml.innerHTML += str;
    }
};

const showSessionID2 = function (data) {
    console.log(data);

    for (let i = 0; i < data.bestemmingen.length; i++) {
        
        sessionidhtml = document.querySelector('.js-sessionid2');

        let str = `
            <option value="${data.bestemmingen[i].RitID}">${data.bestemmingen[i].RitID}</option>
        `;

        sessionidhtml.innerHTML += str;
    }
};

const showSessionID3 = function (data) {
    console.log(data);

    for (let i = 0; i < data.bestemmingen.length; i++) {
        
        sessionidhtml = document.querySelector('.js-sessionid3');

        let str = `
            <option value="${data.bestemmingen[i].RitID}">${data.bestemmingen[i].RitID}</option>
        `;

        sessionidhtml.innerHTML += str;
    }
};

const getSessionId = function (data) {
    showSessionID(data);
};

const getSessionId2 = function (data) {
    showSessionID2(data);
};

const getSessionId3 = function (data) {
    showSessionID3(data);
};

handleData(`http://${lanIP}/api/v1/licht/alleID/`, getSessionId);
handleData(`http://${lanIP}/api/v1/GPS/alleID/`, getSessionId2);
handleData(`http://${lanIP}/api/v1/versnelling/alleID/`, getSessionId3);

// Fetch historical GPS data and update map
const fetchGPS = async function(data) {
    console.log("ontvangen gps data" , data);
    console.log("ontvangen gps.bestemmingen data" , data.bestemmingen);

    let coordinates = [];
    let snelheidList = [];
    let tijd = [];

    if (data.bestemmingen && data.bestemmingen.length > 0) {
        for (let i = 0; i < data.bestemmingen.length; i++) {
            let item2 = data.bestemmingen[i];
            coordinates.push([item2.Coordinaat_Y, item2.Coordinaat_X]);
            snelheidList.push(item2.snelheid);  // Correct the structure here
            tijd.push(new Date(item2.inleesTijd).toLocaleTimeString());
        }
    }

    console.log("dit is de gepuste list coordinaten", coordinates);
    console.log("dit is de gepuste list snelheid", snelheidList);
    console.log("dit is de gepuste list inleestijd gps", tijd);

    updateMapWithHistoricalData(coordinates);
    showChartsSnelheid(snelheidList, tijd);
};

const fetchVersnelling = function (data) {
    console.log("Ontvangen data:", data);
    console.log('dit is .bestemmingen', data.bestemmingen);

    let values2 = [];
    let times2 = [];

    for (let i = 0; i < data.bestemmingen.length; i++) {
        let item3 = data.bestemmingen[i];
        values2.push(item3.versnelling_total);
        times2.push(new Date(item3.InleesTijd).toLocaleTimeString());
    }

    console.log("Dit zijn de values : " ,values2)
    console.log("Dit zijn de tijden : ",times2)

    showChartsVersnelling(values2, times2);
};


// Update map with historical data
const updateMapWithHistoricalData = function(coordinates) {
    // Clear existing route and points
    window.gpsDataList = coordinates;
    window.points = coordinates.map(coord => ({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coord
        }
    }));

    if (window.map.getSource('route')) {
        window.map.getSource('route').setData({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": window.gpsDataList
            }
        });
    }

    if (window.map.getSource('points')) {
        window.map.getSource('points').setData({
            "type": "FeatureCollection",    
            "features": window.points
        });
    }

    // Center the map on the first coordinate if available
    if (coordinates.length > 0) {
        window.map.setCenter(coordinates[0]);
    }
};

const init = function () {
    console.log('domcontentloaded');
    initMap(); // Initialize the map

    document.querySelector('.js-sessionid').addEventListener('change', function () {
        let RitID = this.value;

        console.log(this.value);

        const sessionid = 1;

        console.log('Selected Licht session ID:', RitID);

        handleData(`http://${lanIP}/api/v1/licht/${RitID}/`, fetchLDR);
    }); 

    document.querySelector('.js-sessionid2').addEventListener('change', function () {
        let RitID = this.value;

        console.log(this.value);

        const sessionid = 1;

        console.log('Selected GPS session ID:', RitID);

        handleData(`http://${lanIP}/api/v1/GPS/${RitID}/`, fetchGPS);
    });
        document.querySelector('.js-sessionid3').addEventListener('change', function () {
        let RitID = this.value;

        console.log(this.value);

        const sessionid = 1;

        console.log('Selected Versnelling session ID:', RitID);

        handleData(`http://${lanIP}/api/v1/versnelling/${RitID}/`, fetchVersnelling);
    });
};

document.addEventListener('DOMContentLoaded', init);
