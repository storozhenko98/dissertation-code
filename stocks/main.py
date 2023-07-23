import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from keras.models import load_model

userStock = input("please type the stock you want to predict: ")

# Fetch the data
data = yf.download(userStock, start='2020-01-01', end='2023-01-01')

# Preprocess the data
data = data['Close'].values
data = data.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

# Create training and testing datasets
train_data = data[:int(len(data)*0.8)]
test_data = data[int(len(data)*0.8):]

# Create sequences of data for the LSTM
def create_sequences(data, seq_length):
    xs = []
    ys = []
    for i in range(len(data)-seq_length-1):
        x = data[i:(i+seq_length)]
        y = data[i+seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

seq_length = 5
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# Create the model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile and train the model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, batch_size=1, epochs=1)

# Save the model
model.save('stockModel.h5')



# Function to create sequences of data
def create_sequences(data, seq_length):
    xs = []
    ys = []
    for i in range(len(data)-seq_length-1):
        x = data[i:(i+seq_length)]
        y = data[i+seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

# Load the model
model = load_model('stockModel.h5')

# Fetch the data
data = yf.download(userStock, start='2023-01-01', end='2023-07-23')

# Preprocess the data
data = data['Close'].values
data = data.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

# Create sequences
seq_length = 5  # This should be the same length as when you trained the model
X_test, y_test = create_sequences(data, seq_length)

# Predict the prices
predictions = model.predict(X_test)

# Reverse the scaling for both the predictions and the actual values
predictions = scaler.inverse_transform(predictions)
y_test = scaler.inverse_transform(y_test)

# Calculate the mean squared error
mse = np.mean((predictions - y_test)**2)
print('The Mean Squared Error is:', mse)

# Plot the actual vs predicted values
plt.figure(figsize=(14,5))
plt.plot(y_test, color='red', label=f'Real {userStock} Stock Price')
plt.plot(predictions, color='blue', label=f'Predicted {userStock} Stock Price')
plt.title(f'{userStock} Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel(f'{userStock} Stock Price')
plt.legend()
plt.show()