###  Task 1 - Data analysis workflow and understanding the model and data
## Overview
This task focuses on analyzing the historical Brent oil price dataset to extract meaningful insights, identify key patterns, and understand the modeling techniques used for forecasting. The goal is to preprocess the data, visualize trends, and evaluate different statistical  models for price prediction.

## Steps:

1. Data Collection & Loading

    - Import the Brent oil price dataset from historical records.
    - Load the dataset into pandas for exploration.

2. Exploratory Data Analysis (EDA)

    - Check for missing values and data quality issues.
    - Generate summary statistics (mean, median, standard deviation, etc.).
    - Visualize historical price trends

3. Change Point Detection

    - Identify structural breaks or trend shifts in the time series.
    - Apply statistical tests such as ADF (Augmented Dickey-Fuller) for stationarity analysis.
    - Use algorithms like Bayesian Change Point Detection to detect significant events.

4. Model Understanding & Selection

    - Evaluate statistical models (ARIMA, VAR) for forecasting.
    - Explore deep learning approaches (LSTM) for capturing sequential dependencies.
    - Compare model performance using evaluation metrics (RMSE, MAE, R² score).

## Key Insights from Data Exploration
- Trends & Seasonality: Brent oil prices exhibit seasonal fluctuations influenced by economic and geopolitical factors.
- Stationarity Check: The dataset may require differencing to remove trends for models like ARIMA.
- Change Points: Sudden shifts in prices correspond to historical oil crises and policy changes.

# Development Instructions
- Create a feature/task-1 Branch for development.
- Commit progress regularly with clear and detailed commit messages.
- Merge updates into the main branch via a Pull Request (PR).
