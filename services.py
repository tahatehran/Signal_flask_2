import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from config import Config
from models import CryptoData

class DataService:
    @staticmethod
    def get_crypto_data():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': Config.COINMARKETCAP_API_KEY,
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return DataService.preprocess_data(data)
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching data: {e}")
            return None

    @staticmethod
    def preprocess_data(data):
        coins = data['data']
        for coin in coins:
            if coin['symbol'] == 'BTC':
                processed_data = {
                    'name': coin['name'],
                    'symbol': coin['symbol'],
                    'price': coin['quote']['USD']['price'],
                    'volume_24h': coin['quote']['USD']['volume_24h'],
                    'percent_change_24h': coin['quote']['USD']['percent_change_24h'],
                    'market_cap': coin['quote']['USD']['market_cap']
                }
                CryptoData.add_data(processed_data)
                return processed_data
        return None

class PredictionService:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()

    def train_model(self):
      data = CryptoData.query.order_by(CryptoData.timestamp.desc()).limit(100).all()
      if len(data) < 2:
         raise ValueError("Not enough data to train the model.")
        
      df = pd.DataFrame([d.to_dict() for d in data])
      df['target'] = df['price'].shift(-1)
      df = df.dropna()

      X = df[['price', 'volume_24h', 'percent_change_24h']]
      y = df['target']
    
      X_scaled = self.scaler.fit_transform(X)
      self.model.fit(X_scaled, y)

    def predict(self):
        self.train_model()
        latest_data = CryptoData.query.order_by(CryptoData.timestamp.desc()).first()
        if not latest_data:
            raise ValueError("No data available for prediction.")
            
        X = [[latest_data.price, latest_data.volume_24h, latest_data.percent_change_24h]]
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
      
