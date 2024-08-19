import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


df = pd.read_csv("Mumbai_1990_2022_Santacruz.csv")
df.isnull().sum() # to check no of null items

# to get valid columns
null = df.isnull().sum()/df.shape[0]
valid = df.columns[null < 0.3]

# to store new dataframe
df = df[valid].copy()
df.ffill()
df.info()
df.isnull().sum()

# to fill Nan values
df = df.ffill()
df['tmax'] = df['tmax'].bfill()
df['time'] = pd.to_datetime(df['time'],format='%d-%m-%Y')

# Create columns for today's and tomorrow's temperatures
df['target_temp'] = df['tmax'].shift(-1)  # Predict tomorrow's temperature
df = df.dropna()  # Remove rows with NaN values

features = df[['tmax', 'humidity']].values  # Include humidity as a feature
target = df['target_temp'].values

# Normalize the data
scaler_features = MinMaxScaler()
features_normalized = scaler_features.fit_transform(features)
scaler_target = MinMaxScaler()
target_normalized = scaler_target.fit_transform(target.reshape(-1, 1))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features_normalized, target_normalized, test_size=0.2, shuffle=False)



# Build the model
model = Sequential()
model.add(Dense(64, input_dim=2, activation='relu'))  # Input dimension is 2 because we have two features (temperature and humidity)
model.add(Dense(32, activation='relu'))
model.add(Dense(1))  # Output layer for regression

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mse'])

# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=64,
    validation_split=0.2
)

# evaluate the model
loss = model.evaluate(X_test, y_test)
print(f'Loss: {loss}')

# to save the model
model.save('heat_wave_prediction_model.h5')


