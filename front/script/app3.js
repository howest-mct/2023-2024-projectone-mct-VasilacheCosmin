'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

let sessionid = 0;
let chartLDR, chartMPU;
let ldrData, mpuData = [];
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
        },
        title: {
            text: 'LDR',
            align: 'left',
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'],
                opacity: 0.5,
            },
        },
        xaxis: {
            categories: time,
            labels: {
                show: false,
            },
        },
    };

    chartLDR = new ApexCharts(document.querySelector('.js-chartbpmsession'), options);
    chartLDR.render();
};

const fetchLDR = function (data) {
    let values = data.map((item) => {
        return item.Meting;
    });

    let times = data.map((item) => {
        return new Date(item.InleesTijd).toLocaleTimeString();
    });

    showChartsLDR(values, times);
};

const showSessionID = function (data) {
    const sessionidhtml = document.querySelector('.js-sessionid');
    sessionidhtml.innerHTML = '<option value="">Selecteer een sessie</option>'; // Reset options

    for (let i = 0; i < data.length; i++) {
        console.log(data.bestemmingen[i])
        let str = `<option value="${data[i].RitID}">${data[i].RitID}</option>`;
        sessionidhtml.innerHTML += str;
    }
};

const getSessionId = function (data) {
    // console.log(data);
    showSessionID(data);
};

const handleData = async (url, callback) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    callback(data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

handleData(`http://${lanIP}/api/v1/licht/alleID/`, getSessionId);

const init = function () {
    console.log('domcontentloaded');
    document.querySelector('.js-sessionid').addEventListener('change', function () {
        console.log(this.value)

        const sessionid = 1

        handleData(`http://${lanIP}/api/v1/licht/${sessionid}/`, fetchLDR);
    });
};

document.addEventListener('DOMContentLoaded', init);
