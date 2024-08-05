// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/predict')
        .then(response => response.json())
        .then(data => {
            const chart = LightweightCharts.createChart(document.getElementById('chart'), {
                width: 1000,
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

            const areaSeries = chart.addAreaSeries({
                topColor: 'rgba(67, 83, 254, 0.7)',
                bottomColor: 'rgba(67, 83, 254, 0.3)',
                lineColor: 'rgba(67, 83, 254, 1)',
                lineWidth: 2,
            });

            const volumeSeries = chart.addHistogramSeries({
                color: '#26a69a',
                lineWidth: 2,
                priceFormat: {
                    type: 'volume',
                },
                overlay: true,
            });

            const dataPoints = data.prediction.map((price, index) => ({
                time: Date.now() / 1000 + index * 60,
                value: price,
            }));

            lineSeries.setData(dataPoints);
            areaSeries.setData(dataPoints);

            // Mock volume data
            const volumeData = dataPoints.map(point => ({
                time: point.time,
                value: Math.random() * 1000,
            }));

            volumeSeries.setData(volumeData);
        });
});
