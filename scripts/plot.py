import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense


def priceOverTime(data):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 7))
    plt.plot(data['year'], data['Price'], label='Brent Oil Price')

    plt.xticks(range(min(data['year']), max(data['year']) + 2, 2)) 

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Brent Oil Price Over Time')
    plt.legend()
    plt.show()


def arima(df):
    # Convert 'date' column to datetime and set as index
    df['date'] = pd.to_datetime(df['Date'])
    df = df.set_index('date')

    # Ensure the index is a DatetimeIndex and set daily frequency if not set
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.DatetimeIndex(df.index)
    df['Price'] = df['Price'].fillna(method='ffill')

    # Set frequency to daily if not already inferred
    if df.index.inferred_freq is None:
        df = df.asfreq('D') 

    # Fit the ARIMA model
    model = ARIMA(df['Price'], order=(3, 1, 2))
    fitted_model = model.fit()

    # Forecasting - Modify the periods as needed
    forecast_steps = 30 
    forecast = fitted_model.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

    # Generate forecast and confidence intervals
    forecast_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()

    # Plot the forecast
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Price'], label='Observed', color='blue')
    plt.plot(forecast_index, forecast_values, label='Forecast', color='orange')

    # Confidence interval
    plt.fill_between(forecast_index, confidence_intervals.iloc[:, 0], confidence_intervals.iloc[:, 1], 
                    color='lightgrey', alpha=0.5, label='Confidence Interval')

    # Label forecast points on the chart
    for date, price in zip(forecast_index, forecast_values):
        plt.text(
            date, price, f'{price:.2f}', ha='center', va='bottom', fontsize=8, color='black',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.8)
        )

    plt.title('ARIMA Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    # Print forecast values and dates below the chart
    print("Forecasted Prices:\n")
    for date, price in zip(forecast_index, forecast_values):
        print(f"Date: {date.strftime('%Y-%m-%d')}, Forecasted Price: {price:.2f}")





def garch(data):
    data['date'] = pd.to_datetime(data['Date'])  # Adjust 'Date' if necessary
    data.set_index('date', inplace=True)

    # Calculate the price difference
    data['price_diff'] = data['Price'].diff().dropna()

    # Fit GARCH model to the price differences
    garch_model = arch_model(data['price_diff'].dropna(), vol='Garch', p=1, q=1)
    garch_fit = garch_model.fit(disp='off')

    # Print the summary of the GARCH model
    print(garch_fit.summary())

    # Get the index for the price_diff series
    price_diff_index = data.index[1:]  # Exclude the first index since it corresponds to NaN after differencing

    # Plot the actual price and the conditional volatility
    plt.figure(figsize=(12, 6))

    # Plot actual price
    plt.subplot(2, 1, 1)
    plt.plot(data['Price'], color='blue', label='Actual Price')
    plt.title('Actual Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Plot conditional volatility
    plt.subplot(2, 1, 2)
    plt.plot(price_diff_index, garch_fit.conditional_volatility, color='orange', label='Conditional Volatility')
    plt.title('GARCH Model Conditional Volatility')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()

    plt.tight_layout()
    plt.show()


def all_models(data):
    data['date'] = pd.to_datetime(data['Date'])  # Adjust 'Date' if necessary
    data.set_index('date', inplace=True)

    # Calculate the price difference
    data['price_diff'] = data['Price'].diff().dropna()

    # Fit the ARIMA model to the price differences
    arima_model = ARIMA(data['price_diff'].dropna(), order=(1, 0, 1))  # d=0 since price_diff is already differenced
    fitted_arima = arima_model.fit()

    # Print the summary of the ARIMA model
    print("ARIMA Model Summary:")
    print(fitted_arima.summary())

    # Get the residuals from the ARIMA model
    arima_residuals = fitted_arima.resid

    # Fit the GARCH model to the ARIMA residuals
    garch_model = arch_model(arima_residuals, vol='Garch', p=1, q=1)
    garch_fit = garch_model.fit(disp='off')

    # Print the summary of the GARCH model
    print("GARCH Model Summary:")
    print(garch_fit.summary())

    # Generate ARIMA fitted values
    arima_fitted_values = fitted_arima.fittedvalues

    # Prepare the index for plotting
    price_diff_index = data.index[1:]  # Exclude the first index since it corresponds to NaN after differencing

    # Plot the actual price, ARIMA fitted values, and GARCH conditional volatility
    plt.figure(figsize=(12, 8))

    # Plot actual price
    plt.subplot(3, 1, 1)
    plt.plot(data['Price'], color='blue', label='Actual Price')
    plt.title('Actual Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Plot ARIMA fitted values
    plt.subplot(3, 1, 2)
    plt.plot(price_diff_index, arima_fitted_values, color='green', label='ARIMA Fitted Values')
    plt.title('ARIMA Fitted Values')
    plt.xlabel('Date')
    plt.ylabel('Fitted Price Difference')
    plt.legend()

    # Plot conditional volatility from GARCH model
    plt.subplot(3, 1, 3)
    plt.plot(price_diff_index, garch_fit.conditional_volatility, color='orange', label='Conditional Volatility')
    plt.title('GARCH Model Conditional Volatility')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()

    plt.tight_layout()
    plt.show()


def lstm(data):
    data['date'] = pd.to_datetime(data['Date'])  # Adjust 'Date' if necessary
    data.set_index('date', inplace=True)

    # Calculate the price difference and drop NaNs
    data['price_diff'] = data['Price'].diff().dropna()
    data = data.dropna()  # Drop NaN values from the DataFrame

    # Scale the price difference data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['price_diff'].values.reshape(-1, 1))

    # Prepare the dataset for LSTM
    sequence_length = 60
    X, y = [], []

    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM input

    # Build the LSTM model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(50),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Fit the model with more epochs
    model.fit(X, y, epochs=10, batch_size=32)

    # Generate predictions
    predictions = model.predict(X)
    predictions = scaler.inverse_transform(predictions)

    # Convert predictions back to price levels
    last_price = data['Price'].iloc[-1]  # Get the last actual price
    predicted_prices = last_price + predictions.cumsum(axis=0)  # Cumulative sum of predicted changes

    # Prepare for plotting
    predicted_index = data.index[sequence_length:len(predicted_prices) + sequence_length]

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Price'], label='Actual Price', color='blue')
    plt.plot(predicted_index, predicted_prices, color='red', label='LSTM Prediction')
    plt.title('LSTM Predictions vs Actual Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
