class Config:
    SECRET_KEY = 'your-secret-key-here'  # در یک محیط واقعی، این را در یک متغیر محیطی قرار دهید
    COINMARKETCAP_API_KEY = 'your-coinmarketcap-api-key-here'  # در یک محیط واقعی، این را در یک متغیر محیطی قرار دهید
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crypto.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
