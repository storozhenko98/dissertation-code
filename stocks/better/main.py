import yfinance as yf
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Download 10 years of Apple stock data 
ticker = input("please type the stock you want to predict: ")
data = yf.download(ticker, period='10y')

# Preprocess data
close_prices = data['Close'].values
close_prices = close_prices.reshape(-1, 1) 
scaler = MinMaxScaler(feature_range=(0,1))
close_prices = scaler.fit_transform(close_prices)

# Create samples with 90 day inputs, 2 day targets
inputs = []
targets = []

for i in range(len(close_prices) - 90 - 2):
  inputs.append(close_prices[i:i+90])
  targets.append(close_prices[i+90:i+92])

inputs = np.array(inputs)
targets = np.array(targets)

# Split into train/test sets
train_split = 0.8
train_size = int(train_split * len(inputs))
train_inputs = inputs[:train_size]
train_targets = targets[:train_size] 
test_inputs = inputs[train_size:]
test_targets = targets[train_size:]

# Reshape input data into 3D format 
train_inputs = train_inputs.reshape(train_inputs.shape[0], train_inputs.shape[1], 1)
test_inputs = test_inputs.reshape(test_inputs.shape[0], test_inputs.shape[1], 1)

# Build LSTM model
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(50, activation='relu', input_shape=(90,1))) 
model.add(tf.keras.layers.Dense(2))
model.compile(optimizer='adam', loss='mse')

# Train model
model.fit(train_inputs, train_targets, epochs=10, validation_data=(test_inputs, test_targets))

# Evaluate on test set 
test_preds = model.predict(test_inputs)
test_perf = model.evaluate(test_inputs, test_targets) 
test_loss = model.evaluate(test_inputs, test_targets)
print("Test Loss: {:.4f}".format(test_loss))

# Make prediction
close_prices_recent = close_prices[-90:]
close_prices_recent = close_prices_recent.reshape(1,90,1)
price_pred = model.predict(close_prices_recent)[0]
price_pred = scaler.inverse_transform([price_pred]) 
print("Predicted closing price 2 days later: {}".format(price_pred))