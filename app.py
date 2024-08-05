from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

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

@app.route('/')
def index():
    data = get_crypto_data()
    # Process data to get relevant information
    return render_template('index.html', data=data)

@app.route('/api/predict', methods=['GET'])
def predict():
    # Load the pre-trained model
    model = joblib.load('models/prediction_model.pkl')
    # Get the current data for prediction
    data = get_crypto_data()
    # Assume we process data to create a feature vector X
    X = ...  # Processed data to feed into model
    prediction = model.predict(X)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
