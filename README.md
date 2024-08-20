
# Summer Heat Wave Mobile Alert System

This project is a Summer Heat Wave Mobile Alert System that predicts the likelihood of a heat wave based on historical temperature and humidity data. The system provides real-time SMS notifications to users, helping them stay informed and take necessary precautions during extreme weather conditions.




## Features

- **Heat Wave Prediction:** Utilizes a feedforward neural network (Multi-Layer Perceptron) model to predict the possibility of a heat wave based on temperature and humidity data.
- **Real-Time SMS Alerts:** Sends SMS notifications to users in real-time using Twilio when a heat wave is predicted.
- **User-Friendly Interface:** Built with Streamlit to provide a simple and intuitive GUI for interacting with the model and receiving predictions.



## Project Structure

- `heat_wave_prediction_model.h5`: The trained deep learning model for predicting heat waves.
- `main.py`: The main Streamlit application that serves as the GUI.
- `requirements.txt`: List of required Python packages for running the project.
- `README.md`: This file, containing an overview of the project and instructions for setup.

## Dataset
The dataset used for training and testing the model was obtained from [Kaggle](https://www.kaggle.com/datasets/vanvalkenberg/historicalweatherdataforindiancities). It includes historical temperature and humidity data across various cities. For this project, the dataset from Mumbai city was used.

## Installation
1. Clone the repository:
   ```bash 
    https://github.com/yash-jagtap1706/Summer_heat_wave_alert_system.git
    ```

2. Install the required Python packages:

 ```bash
pip install -r requirements.txt
```

3. Set up your Twilio account and add your credentials to the .env file:
```bash
account_sid=your_account_sid
auth_token=your_auth_token
from_phone_number=your_twilio_phone_number
weather_api_key=your_weather_api_key
```
4. Run the Streamlit app:
```bash
streamlit run app.py
```

 
## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License - see the [LICENSE](LICENSE) file for details.



## Contact

For any questions or issues, please contact yvj0007@gmail.com
