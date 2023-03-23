install pips
```
!pip install numpy 
!pip install requests
!pip install scikit-learn
!pip install prophet
```

btc script
```
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet


# Function to retrieve historical Bitcoin price data from Alpha Vantage
def get_historical_data():
    api_key = 'apikeyhere'
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    historical_data = {}

    for date, entry in data['Time Series (Digital Currency Daily)'].items():
        timestamp = datetime.strptime(date, '%Y-%m-%d')
        price_usd = float(entry['4a. close (USD)'])
        historical_data[timestamp] = price_usd
    return historical_data

# Rest of the code remains the same
# Function to convert the historical data to a feature matrix and target vector
def historical_data_to_dataframe(historical_data):
    timestamps = sorted(list(historical_data.keys()))
    prices = [historical_data[timestamp] for timestamp in timestamps]
    data = {'ds': timestamps, 'y': prices}
    return pd.DataFrame(data)

def make_prediction(model, latest_data, days_into_future):
    future = model.make_future_dataframe(periods=days_into_future)
    forecast = model.predict(future)
    prediction = forecast.tail(days_into_future)['yhat'].values
    return prediction

def main():
    # Get historical Bitcoin price data from CoinMarketCap
    historical_data = get_historical_data()

    # Convert the historical data to a DataFrame
    df = historical_data_to_dataframe(historical_data)

    # Train a Prophet model on the DataFrame
    model = Prophet()
    model.fit(df)

    # Use the model to make predictions
    days_into_future_tomorrow = 1
    days_into_future_next_week = 7
    days_into_future_next_month = 30
    prediction_tomorrow = make_prediction(model, df, days_into_future_tomorrow)
    prediction_next_week = make_prediction(model, df, days_into_future_next_week)
    prediction_next_month = make_prediction(model, df, days_into_future_next_month)

    # Print or process the predictions
    print("Predicted price for tomorrow:", prediction_tomorrow[0])
    print("Predicted price for next week:", prediction_next_week[-1])
    print("Predicted price for next month:", prediction_next_month[-1])

if __name__ == '__main__':
    main()
    ```
    
    
demo output
    
```
Predicted price for tomorrow: 27820.884665193036
Predicted price for next week: 28322.56187457725
Predicted price for next month: 22543.705880921414
```
