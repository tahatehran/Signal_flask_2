import unittest
from app import app, db
from models import CryptoData
from services import DataService, PredictionService

class TestCryptoApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_predict_route(self):
        response = self.app.get('/api/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.json)

    def test_data_service(self):
        data = DataService.get_crypto_data()
        self.assertIsNotNone(data)
        self.assertIn('name', data)
        self.assertIn('price', data)

    def test_prediction_service(self):
        # Add some dummy data
        with app.app_context():
            for i in range(100):
                CryptoData.add_data({
                    'name': 'Bitcoin',
                    'symbol': 'BTC',
                    'price': 50000 + i * 100,
                    'volume_24h': 1000000000,
                    'percent_change_24h': 1,
                    'market_cap': 1000000000000
                })

        prediction_service = PredictionService()
        prediction = prediction_service.predict()
        self.assertIsNotNone(prediction)

if __name__ == '__main__':
    unittest.main()
