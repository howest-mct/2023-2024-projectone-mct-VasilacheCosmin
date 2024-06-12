"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

let sessionid = 0;

let chartLDR, chartMPU; //,chartAir;

let sessionidhtml;

let ldrData, mpuData = [];//, airData = [];
let chartTime = [];

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

const getSessionId = function (data) {
    showSessionID(data);
};

handleData(`http://${lanIP}/api/v1/licht/alleID/`, getSessionId);

// Fetch historical GPS data and update map
const fetchGPSData = async function(RitID) {
    const response = await fetch(`http://${lanIP}/api/v1/gps/${RitID}/`);
    const data = await response.json();

    let coordinates = [];
    if (data.bestemmingen && data.bestemmingen.length > 0) {
        for (let i = 0; i < data.bestemmingen.length; i++) {
            let item = data.bestemmingen[i];
            coordinates.push([item.lon, item.lat]);
        }
    }

    updateMapWithHistoricalData(coordinates);
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
    document.querySelector('.js-sessionid').addEventListener('change', function () {
        let RitID = this.value;

        console.log(this.value);

        const sessionid = 1;

        console.log('Selected session ID:', RitID);

        handleData(`http://${lanIP}/api/v1/licht/${RitID}/`, fetchLDR);
        fetchGPSData(RitID);  // Fetch and display GPS data for the selected ID
    });
};

document.addEventListener('DOMContentLoaded', init);
