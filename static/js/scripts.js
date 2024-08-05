// static/js/scripts.js

fetch('/api/predict')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('cryptoChart').getContext('2d');
        const cryptoChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [...Array(data.prediction.length).keys()],
                datasets: [{
                    label: 'Crypto Prices Prediction',
                    data: data.prediction,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
