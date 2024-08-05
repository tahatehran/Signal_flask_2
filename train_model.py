import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load historical data
data = pd.read_csv('data/coin_data.csv')

# Feature engineering
X = data[['price', 'volume_24h', 'percent_change_24h']]  # Features
y = data['future_price']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model
joblib.dump(model, 'models/prediction_model.pkl')
print("Model saved to models/prediction_model.pkl")
