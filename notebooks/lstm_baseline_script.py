# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# # LSTM Baseline Model for Stock Price Prediction

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# ## 1. Load and Prepare the Data

# Load the dataset
DATA_PATH = 'data/AAPL_stock_data.csv'
# The yfinance data has a header row and then a row with the ticker.
# We can skip the second row (the ticker row) by using skiprows=[1]
df = pd.read_csv(DATA_PATH)
df = df.iloc[1:].reset_index(drop=True)


# Use the 'Close' price for prediction and convert to numeric
data = df.filter(['Close'])
data['Close'] = pd.to_numeric(data['Close'])
dataset = data.values
training_data_len = int(np.ceil(len(dataset) * .8))

# Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

# ## 2. Create Training Data

# Create the training data set
train_data = scaled_data[0:int(training_data_len), :]

# Split the data into x_train and y_train data sets
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])

# Convert the x_train and y_train to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# ## 3. Build the LSTM Model

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# ## 4. Compile and Train the Model

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=1)

# ## 5. Create Test Data

# Create the testing data set
test_data = scaled_data[training_data_len - 60:, :]

# Create the x_test and y_test data sets
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

# Convert the data to a numpy array
x_test = np.array(x_test)

# Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# ## 6. Make Predictions

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# ## 7. Visualize the Results

train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.savefig('data/lstm_baseline_predictions.png')
print("Plot of predictions saved to data/lstm_baseline_predictions.png")
