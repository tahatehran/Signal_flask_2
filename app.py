from flask import Flask, render_template, jsonify
from config import Config
from models import db, CryptoData
from services import DataService, PredictionService
from utils import get_buy_sell_signals

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    data = CryptoData.query.order_by(CryptoData.timestamp.desc()).first()
    if not data:
        data = DataService.get_crypto_data()
    else:
        data = data.to_dict()

    if data:
        processed_data = get_buy_sell_signals(data)
    else:
        processed_data = {}
        
    return render_template('index.html', data=processed_data)

@app.route('/api/predict', methods=['GET'])
def predict():
    prediction_service = PredictionService()
    prediction = prediction_service.predict()
    return jsonify({'prediction': prediction.tolist()})
