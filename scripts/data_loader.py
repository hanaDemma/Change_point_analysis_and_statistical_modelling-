import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose  # type: ignore


def loadData():
    """
       Loads a CSV file into a Pandas DataFrame.

       Returns:
           pd.DataFrame: DataFrame containing the loaded data.
       """
    return pd.read_csv('docs/BrentOilPrices.csv')

# def loadData():
#     return pd.read_csv('./docs/BrentOilPrices.csv')
# def oilPricOverTime(price_data):
#     plt.figure(figsize=(12, 6))
#     plt.plot(price_data['Price'])
#     plt.title("Brent Oil Prices Over Time")
#     plt.xlabel("Date")
#     plt.ylabel("Price (USD/barrel)")
#     plt.show()