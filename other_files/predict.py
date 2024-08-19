import tensorflow as tf
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib
import warnings
warnings.filterwarnings('ignore')

# Suppress TensorFlow warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Optionally, use TensorFlow's logging control
tf.get_logger().setLevel('ERROR')

model = tf.keras.models.load_model(f"D:\\Summer heat wave prediction\\model\\heat_wave_prediction_model.keras")
scaler_features = joblib.load(f"D:\\Summer heat wave prediction\\model\\scaler_features.pkl")
scaler_target = joblib.load(f'D:\\Summer heat wave prediction\\model\\scaler_target.pkl')

def predict_tomorrow_temperature(today_temp, today_humidity):
    # Prepare input data
    input_data = np.array([[today_temp, today_humidity]])
    input_data_normalized = scaler_features.transform(input_data)

    # Predict tomorrow's temperature
    tomorrow_temp_normalized = model.predict(input_data_normalized)
    tomorrow_temp = scaler_target.inverse_transform(tomorrow_temp_normalized)

    return tomorrow_temp[0][0]


# Example: Predict tomorrow's temperature given today's temperature and humidity
today_temp = 32  # Example temperature value
today_humidity = 77  # Example humidity value
predicted_tomorrow_temp = predict_tomorrow_temperature(today_temp, today_humidity)
print(f'Predicted Temperature for Tomorrow: {predicted_tomorrow_temp}°C')