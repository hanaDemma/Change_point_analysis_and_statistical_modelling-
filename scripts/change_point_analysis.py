import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose  # type: ignore
import pymc as pm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from prophet import Prophet
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense # type: ignore
from statsmodels.tsa.api import VAR


import pymc as pm

def change_point_analysis(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by='Date').reset_index(drop=True)

    change_points = []
    significant_change_points = []
    min_distance = 100 
    mean_diff_threshold = 10 
    significant_mean_diff_threshold = 20

    peaks, _ = find_peaks(data['Price'], distance=min_distance)
    troughs, _ = find_peaks(-data['Price'], distance=min_distance)

    extrema = sorted(np.concatenate((peaks, troughs)))

    for i in range(min_distance, len(data) - min_distance):
        before_data = data['Price'][:i]
        after_data = data['Price'][i:]
        
        mean_before = before_data.mean()
        mean_after = after_data.mean()
        
        if abs(mean_before - mean_after) > significant_mean_diff_threshold:
            if not significant_change_points or (i - significant_change_points[-1] >= min_distance):
                significant_change_points.append(i)
        elif abs(mean_before - mean_after) > mean_diff_threshold:
            if not change_points or (i - change_points[-1] >= min_distance):
                change_points.append(i)

    all_change_points = sorted(set(change_points + extrema))
    all_significant_change_points = sorted(set(significant_change_points + extrema))

    results = {
        'Type': [],
        'Date': [],
        'Price': []
    }

    # Define key events with additional significant dates
    key_events = {
        pd.to_datetime('1987-10-19'): '1987 Stock Market Crash',
        pd.to_datetime('1990-08-02'): '1990 Gulf War',
        pd.to_datetime('1997-07-01'): '1997 Asian Financial Crisis',
        pd.to_datetime('1998-12-10'): '1998 Asian Financial Crisis',
        pd.to_datetime('2001-09-11'): '2001 9/11 Attacks',
        pd.to_datetime('2003-03-20'): '2003 Iraq War',
        pd.to_datetime('2005-08-29'): '2005 Hurricane Katrina',
        pd.to_datetime('2008-11-24'): '2008 Financial Crisis',
        pd.to_datetime('2011-01-25'): '2011 Arab Spring',
        pd.to_datetime('2011-02-15'): '2011 Libyan Civil War',
        pd.to_datetime('2014-06-01'): '2014 ISIS Advancements in Iraq',
        pd.to_datetime('2014-11-27'): '2014 Oil Price Crash',
        pd.to_datetime('2016-11-30'): '2016 OPEC Production Cut',
        pd.to_datetime('2020-04-21'): '2020 COVID-19 Pandemic',
        pd.to_datetime('2021-02-14'): '2021 Texas Winter Storm',
        pd.to_datetime('2022-03-08'): '2022 Geopolitical Tensions (Russian-Ukraine)'
    }

    def plot_segment(data, start_idx, end_idx, change_points, significant_change_points):
        plt.figure(figsize=(14, 7))
        plt.plot(data['Date'][start_idx:end_idx], data['Price'][start_idx:end_idx], label='Brent Oil Price')
        
        for cp in change_points:
            if start_idx <= cp < end_idx:
                plt.axvline(x=data['Date'].iloc[cp], color='orange', linestyle='--', label='Detected Change Point')
                plt.annotate(f"{data['Date'].iloc[cp].date()}\n{data['Price'].iloc[cp]:.2f}", 
                            xy=(data['Date'].iloc[cp], data['Price'].iloc[cp]), 
                            xytext=(5, 5), textcoords='offset points', 
                            arrowprops=dict(arrowstyle='->', color='orange'),
                            fontsize=10, color='orange')

        for scp in significant_change_points:
            if start_idx <= scp < end_idx:
                plt.axvline(x=data['Date'].iloc[scp], color='red', linestyle='--', label='Significant Change Point')
                plt.annotate(f"{data['Date'].iloc[scp].date()}\n{data['Price'].iloc[scp]:.2f}", 
                            xy=(data['Date'].iloc[scp], data['Price'].iloc[scp]), 
                            xytext=(5, -15), textcoords='offset points', 
                            arrowprops=dict(arrowstyle='->', color='red'),
                            fontsize=10, color='red')

        # Annotate key events
        for event_date, event_name in key_events.items():
            event_rows = data[data['Date'] == event_date]
            if not event_rows.empty:  # Check if the filtered DataFrame is not empty
                plt.annotate(event_name, xy=(event_date, event_rows['Price'].values[0]), 
                            xytext=(5, -25), textcoords='offset points',
                            fontsize=10, color='purple', bbox=dict(facecolor='white', alpha=0.5))

        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'Brent Oil Prices from {data["Date"].iloc[start_idx]} to {data["Date"].iloc[end_idx-1]}')
        plt.legend()
        plt.show()


    segment_size = 500

    for i in range(0, len(data), segment_size):
        start_idx = i
        end_idx = min(i + segment_size, len(data))
        plot_segment(data, start_idx, end_idx, change_points, significant_change_points)

    for cp in all_change_points:
        results['Type'].append('Change Point')
        results['Date'].append(data['Date'].iloc[cp].date())
        results['Price'].append(data['Price'].iloc[cp])

    for scp in all_significant_change_points:
        results['Type'].append('Significant Change Point')
        results['Date'].append(data['Date'].iloc[scp].date())
        results['Price'].append(data['Price'].iloc[scp])

    results_df = pd.DataFrame(results)

    results_df.to_csv('./docs/change_points.csv', index=False)

    print("Detected Change Points and Significant Change Points have been saved to 'docs/change_points.csv'.")


def changePointDetection(price_data):
    prices = price_data['Price'].values
    n = len(prices)

    with pm.Model() as model:
        change_point = pm.DiscreteUniform("change_point", lower=0, upper=n)

        mean1 = pm.Normal("mean1", mu=np.mean(prices[:n//2]), sigma=np.std(prices[:n//2]))
        mean2 = pm.Normal("mean2", mu=np.mean(prices[n//2:]), sigma=np.std(prices[n//2:]))
        sigma = pm.HalfNormal("sigma", sigma=10)

        idx = np.arange(n)
        mean = pm.math.switch(idx < change_point, mean1, mean2)
        obs = pm.Normal("obs", mu=mean, sigma=sigma, observed=prices)

        trace = pm.sample(1500, tune=1500, target_accept=0.95, chains=4)

    pm.plot_trace(trace,figsize=(20,20))
    plt.show()

def autoCorrAndPartialAutoCorr(price_data):
    plt.figure(figsize=(12, 6))
    plot_acf(price_data['Price'], lags=40)
    plt.show()

    plt.figure(figsize=(12, 6))
    plot_pacf(price_data['Price'], lags=40)
    plt.show()

def arimaModel(price_data,test):
    # order(p,d,q)
    arima_model = ARIMA(price_data['Price'], order=(1, 1, 1)) 
    arima_result = arima_model.fit()
    print(arima_result.summary())

    # Forecasting
    arima_forecast = arima_result.forecast(steps=len(test))
    return arima_forecast