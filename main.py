import streamlit as st
import tensorflow as tf
import numpy as np
import joblib
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()


# Load models and scalers
model = tf.keras.models.load_model("model/heat_wave_prediction_model.keras")
scaler_features = joblib.load('model/scaler_features.pkl')
scaler_target = joblib.load('model/scaler_target.pkl')
heat_wave_threshold = 32

header = {
    "account_sid" : st.secrets["account_sid"],
    "auth_token": st.secrets["auth_token"],
    "weather_api_key": st.secrets["weather_api_key"],
    "from_phone_number": st.secrets["from_no"]

}

# # Load API keys from environment variables
# account_sid = os.getenv("account_sid")
# auth_token = os.getenv("auth_token")
# weather_api_key = os.getenv("weather_api_key")
# from_phone_number = os.getenv("from_no")

account_sid = header["account_sid"]
auth_token = header["auth_token"]
weather_api_key = header["weather_api_key"]
from_phone_number = header["from_phone_number"]

client = Client(account_sid, auth_token)

# Initialize session state if it doesn't exist
if st.session_state.get("clear"):
    st.session_state['name'] = ""
    st.session_state['number'] = ""


# Helper functions
def get_current_temp_humidity(city='Mumbai'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = round(data['main']['temp'], 1)
        humidity = round(data['main']['humidity'], 1)
        return temperature, humidity
    else:
        st.error('Failed to retrieve weather data')
        return None, None


def predict_tomorrow_temperature(today_temp, today_humidity):
    input_data = np.array([[today_temp, today_humidity]])
    input_data_normalized = scaler_features.transform(input_data)
    tomorrow_temp_normalized = model.predict(input_data_normalized)
    tomorrow_temp = scaler_target.inverse_transform(tomorrow_temp_normalized)
    return tomorrow_temp[0][0]


def send_alerts(message, to_phone_number):
    from_phone_number = os.getenv("from_no")
    # from_phone_number = '6503835249'
    message = client.messages.create(
        body=message,
        from_=from_phone_number,
        to=to_phone_number
    )
    return message.sid


def main_work(to, name):
    to_phone_number = "+91" + to
    temp, humidity = get_current_temp_humidity()
    predicted_tomorrow_temp = predict_tomorrow_temperature(temp, humidity)
    alert_message = f"Hi {name}, Heatwave Alert! Temperatures are expected to exceed {heat_wave_threshold}°C tomorrow. Stay hydrated and indoors. Predicted temperature: {predicted_tomorrow_temp:.2f}°C"
    mess = f"Good news {name}! No heat wave expected tomorrow. Predicted temperature: {predicted_tomorrow_temp:.2f}°C. Enjoy your day!"
    if temp is not None and humidity is not None:
        # sleep(4)
        if predicted_tomorrow_temp >= heat_wave_threshold:
            st.write(alert_message)
            alert_sid = send_alerts(alert_message,to_phone_number)
            # print(f"Alert sent with SID: {alert_sid}")
        else:
            st.write(mess)
            alert_sid = send_alerts(mess,to_phone_number)
            # print(f"Alert sent with SID: {alert_sid}")
    else:
        st.error("Failed to retrieve current weather data.")


# Main app code
st.sidebar.write("Dashboard")
page_selected = st.sidebar.selectbox("Select page", ["Home", "Heat Wave Alert", "About us"])

if page_selected == "Home":
    st.header("Heat Wave Alert System")
    img_path = f"D:\\Projects\\Task_3\\asset\\home.jpg"
    st.image(img_path, use_column_width=True)
    st.markdown("""
    # Welcome to the Heat Wave Alert System! 🌡️📱

    ## Overview
    This web app provides timely heat wave alerts by predicting tomorrow's temperature and notifying users via SMS. Simply enter your phone number to receive alerts about potential heat waves directly to your phone.

    ### How It Works
    1. **Enter Phone Number:** Go to the **Heat Wave Alert** page and input your phone number.
    2. **Prediction & Alert:** Our system will use advanced deep learning techniques to predict tomorrow's temperature and send you an alert if a heat wave is expected.
    3. **Stay Informed:** Receive real-time updates and stay safe during extreme weather conditions.

    ### Why Choose Us?
    - **Accuracy:** We leverage deep learning techniques for precise temperature predictions and heat wave alerts.
    - **User-Friendly:** Our intuitive interface ensures a seamless and straightforward user experience.
    - **Quick Alerts:** Get timely notifications to make informed decisions and prepare for heat waves.

    ### About Us
    Learn more about the project, our team, and our mission on the **About Us** page.
    """)

elif page_selected == "Heat Wave Alert":
    st.header("Heat Wave Alert System")

    user_name = st.text_input("Enter your name:",key="name")
    ph_number = st.text_input("Enter phone number to receive alerts:",key="number")

    if st.button("Submit"):
        if ph_number and user_name:
            main_work(ph_number,user_name)
            st.button("Clear", key="clear")

elif page_selected == "About us":
    st.header("About Us")
    st.markdown("""
    ### About Dataset
    This dataset is sourced from Kaggle and includes historical weather data for Indian cities from 1990 to 2022. The dataset provides detailed information on temperature and other weather-related metrics across various cities, making it ideal for predicting heat waves and analyzing temperature trends.

    #### Dataset Overview 
    - **Source**: Kaggle
    - **Coverage**: Weather data for Indian cities
    - **Time Span**: 1990 to 2022
    """)
