from flask import Flask, render_template, jsonify
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

app = Flask(__name__)

# API Key for CoinMarketCap
API_KEY = 'key'

# Endpoint for CoinMarketCap
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

def get_crypto_data():
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    response = requests.get(URL, headers=headers)
    data = response.json()
    return data

def preprocess_data(data):
    # Simple preprocessing example
    coins = data['data']
    processed_data = []
    for coin in coins:
        processed_data.append({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'price': coin['quote']['USD']['price'],
            'volume_24h': coin['quote']['USD']['volume_24h'],
            'percent_change_24h': coin['quote']['USD']['percent_change_24h']
        })
    return pd.DataFrame(processed_data)

def train_model(data):
    data = data.dropna()  # Drop any rows with missing values
    X = data[['price', 'volume_24h', 'percent_change_24h']]
    y = data['price'].shift(-1).fillna(data['price'])  # Future price prediction

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)
    return model, scaler

@app.route('/')
def index():
    data = get_crypto_data()
    processed_data = preprocess_data(data)
    return render_template('index.html', data=processed_data.to_dict(orient='records'))

@app.route('/api/predict', methods=['GET'])
def predict():
    data = get_crypto_data()
    processed_data = preprocess_data(data)
    model, scaler = train_model(processed_data)
    X = processed_data[['price', 'volume_24h', 'percent_change_24h']]
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
