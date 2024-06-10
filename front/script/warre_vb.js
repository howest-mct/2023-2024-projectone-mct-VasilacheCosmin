'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

let sessionid = 0;

let chartLDR, chartMPU; //,chartAir;

// chartLDR.updateOptions( {
//   xaxis: {
//     categories: []
//   },
//   series: {
//     name: "LDR",
//     data: []
//   }
// });

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


//
//const showChartsMPU = function (data, time) {
//    mpuData = data;
//    chartTime = time;
//
//    if (chartMPU) {
//        chartMPU.destroy();
//    }
//
//    let options = {
//        series: [
//            {
//                name: 'MPU',
//                data: data,
//            },
//        ],
//        chart: {
//            height: 200,
//            type: 'line',
//            zoom: {
//                enabled: false,
//            },
//        },
//        dataLabels: {
//            enabled: false,
//        },
//        stroke: {
//            curve: 'straight',
//        },
//        title: {
//            text: 'MPU',
//            align: 'left',
//        },
//        grid: {
//            row: {
//                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
//                opacity: 0.5,
//            },
//        },
//        xaxis: {
//            categories: time,
//            labels: {
//                show: false,
//            },
//        },
//    };
//
//    chartMPU = new ApexCharts(document.querySelector('.js-charttempsession'), options);
//    chartMPU.render();
//};

//const showChartsAir = function (data, time) {
//    airData = data;
//    chartTime = time;
//
//    if (chartAir) {
//        chartAir.destroy();
//    }
//
//    let options = {
//        series: [
//            {
//                name: 'Air Quality',
//                data: data,
//            },
//        ],
//        chart: {
//            height: 200,
//            type: 'line',
//            zoom: {
//                enabled: false,
//            },
//        },
//        dataLabels: {
//            enabled: false,
//        },
//        stroke: {
//            curve: 'straight',
//        },
//        title: {
//            text: 'Air Quality',
//            align: 'left',
//        },
//        grid: {
//            row: {
//                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
//                opacity: 0.5,
//            },
//        },
//        xaxis: {
//            categories: time,
//            labels: {
//                show: false,
//            },
//        },
//    };
//
//    chartAir = new ApexCharts(document.querySelector('.js-chartairsession'), options);
//    chartAir.render();
//};
//
const fetchLDR = function (data) {
    console.log("Ontvangen data:", data);
    console.log('dit is .bestemmingen', data.bestemmingen);
    console.log(data.bestemmingen.length)
    console.log(data.bestemmingen[1].InleesTijd)
    let test = data.bestemmingen[1]

    console.log(test.InleesTijd)
    console.log(test.Meting)
 
    let values = [];
    let times = [];

    for (let i = 0; i < data.bestemmingen.length; i++) {
        let item = data.bestemmingen[i];
        values.push(item.Meting);
        times.push(new Date(item.InleesTijd).toLocaleTimeString());
    }

    console.log(values)
    console.log(times)

    showChartsLDR(values, times);
};
//
//const fetchMPU = function (data) {
//    let values = data.map((item) => {
//        return item.Value;
//    });
//
//    let times = data.map((item) => {
//        return new Date(item.ActionDate).toLocaleTimeString();
//    });
//
//    showChartsMPU(values, times);
//};

//const fetchAir = function (data) {
//    let values = data.map((item) => {
//        return item.Value;
//    });
//
//    let times = data.map((item) => {
//        return new Date(item.ActionDate).toLocaleTimeString();
//    });
//
//    showChartsAir(values, times);
//};

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
    // console.log(data);
    showSessionID(data);
};

handleData(`http://${lanIP}/api/v1/licht/alleID/`, getSessionId);

const init = function () {
    console.log('domcontentloaded');
    document.querySelector('.js-sessionid').addEventListener('change', function () {
        let RitID = this.value;

        console.log(this.value)

        const sessionid = 1

        
        console.log('Selected session ID:', RitID);

        handleData(`http://${lanIP}/api/v1/licht/${RitID}/`, fetchLDR);
        //handleData(`http://${lanIP}/api/v1/history/${sessionid}/temp/`, fetchMPU);
        //handleData(`http://${lanIP}/api/v1/history/${sessionid}/air/`, fetchAir);
    });
};

document.addEventListener('DOMContentLoaded', init);
