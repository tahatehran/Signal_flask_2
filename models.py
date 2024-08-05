from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CryptoData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100))
    symbol = db.Column(db.String(10))
    price = db.Column(db.Float)
    volume_24h = db.Column(db.Float)
    percent_change_24h = db.Column(db.Float)
    market_cap = db.Column(db.Float)

    @staticmethod
    def add_data(data):
        new_data = CryptoData(**data)
        db.session.add(new_data)
        db.session.commit()

    def to_dict(self):
        return {
            'name': self.name,
            'symbol': self.symbol,
            'price': self.price,
            'volume_24h': self.volume_24h,
            'percent_change_24h': self.percent_change_24h,
            'market_cap': self.market_cap,
            'timestamp': self.timestamp.isoformat()
        }
      
