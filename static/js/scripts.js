document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/predict')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('priceChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Current', 'Predicted'],
                    datasets: [{
                        label: 'Bitcoin Price',
                        data: [parseFloat(document.getElementById('currentPrice').textContent), data.prediction[0]],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
});
