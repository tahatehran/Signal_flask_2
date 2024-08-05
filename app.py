from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

app = Flask(__name__)

# API Key for CoinMarketCap
API_KEY = 'your_coinmarketcap_api_key'

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

@app.route('/')
def index():
    data = get_crypto_data()
    processed_data = preprocess_data(data)
    return render_template('index.html', data=processed_data.to_dict(orient='records'))

@app.route('/api/predict', methods=['GET'])
def predict():
    model = joblib.load('models/prediction_model.pkl')
    data = get_crypto_data()
    processed_data = preprocess_data(data)
    X = processed_data[['price', 'volume_24h', 'percent_change_24h']]
    prediction = model.predict(X)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)

