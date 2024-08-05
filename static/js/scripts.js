// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/predict')
        .then(response => response.json())
        .then(data => {
            const chart = LightweightCharts.createChart(document.getElementById('chart'), {
                width: document.getElementById('chart').clientWidth,
                height: 600,
                layout: {
                    backgroundColor: '#ffffff',
                    textColor: '#333',
                },
                grid: {
                    vertLines: {
                        color: '#eee',
                    },
                    horzLines: {
                        color: '#eee',
                    },
                },
                crosshair: {
                    mode: LightweightCharts.CrosshairMode.Normal,
                },
                rightPriceScale: {
                    borderColor: '#ccc',
                },
                timeScale: {
                    borderColor: '#ccc',
                },
            });

            const lineSeries = chart.addLineSeries({
                color: 'rgba(4, 111, 232, 1)',
                lineWidth: 2,
            });

            const dataPoints = data.prediction.map((price, index) => ({
                time: Date.now() / 1000 + index * 60,
                value: price,
            }));

            lineSeries.setData(dataPoints);
        });
});
