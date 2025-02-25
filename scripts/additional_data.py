import pandas as pd
import wbdata
import datetime
import matplotlib.pyplot as plt
import seaborn as sns



start_date = datetime.datetime(1987, 1, 1)
end_date = datetime.datetime(2022, 12, 31)
countries = ['USA', 'ETH', 'GBR', 'ZAF', 'BRA', 'CHN'] 


def gdp_data(start_date,end_date):
    countries = ['USA', 'ETH', 'GBR', 'ZAF', 'BRA', 'CHN'] 

    # Fetch GDP data for the countries
    gdp_data = wbdata.get_dataframe({'NY.GDP.MKTP.CD': 'GDP'}, country=countries)
    gdp_data.reset_index(inplace=True)

    # Convert 'date' column to datetime
    gdp_data['date'] = pd.to_datetime(gdp_data['date'])

    # Filter the GDP data to only include data from 1987 onwards
    gdp_data = gdp_data[(gdp_data['date'] >= start_date) & (gdp_data['date'] <= end_date)]

    # Split the data for Brazil and the other countries
    brazil_gdp = gdp_data[gdp_data['country'] == 'Brazil']
    other_gdp = gdp_data[gdp_data['country'] != 'Brazil']

    # Set up the figure and axes for the subplots
    fig, axs = plt.subplots(2, 1, figsize=(14, 10))

    # Plotting GDP for Brazil
    sns.lineplot(data=brazil_gdp, x='date', y='GDP', color='orange', ax=axs[0])
    axs[0].set_title('GDP Over Time for Brazil')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('GDP in Billions')
    axs[0].tick_params(axis='x', rotation=65)  

    # Plotting GDP for other countries
    sns.lineplot(data=other_gdp, x='date', y='GDP', hue='country', palette='Set2', ax=axs[1])
    axs[1].set_title('GDP Over Time for Other Countries')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('GDP in Billions')
    axs[1].tick_params(axis='x', rotation=65)  
    axs[1].legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout
    plt.tight_layout()
    plt.show()

    return gdp_data


def inflation_data(start_date,end_date):
    # Fetch Inflation data (Consumer Prices, Annual %)
    inflation_data = wbdata.get_dataframe({'FP.CPI.TOTL.ZG': 'Inflation'}, country=countries)
    inflation_data.reset_index(inplace=True)

    # Convert 'date' column to datetime and filter for 1987–2022
    inflation_data['date'] = pd.to_datetime(inflation_data['date'])
    inflation_data = inflation_data[(inflation_data['date'] >= start_date) & (inflation_data['date'] <= end_date)]

    # Display the Inflation data
    brazil_inflation = inflation_data[inflation_data['country'] == 'Brazil']
    other_inflation = inflation_data[inflation_data['country'] != 'Brazil']

    # Set up the figure and axes for the subplots
    fig, axs = plt.subplots(2, 1, figsize=(14, 10))

    # Plotting Inflation for Brazil
    sns.lineplot(data=brazil_inflation, x='date', y='Inflation', color='orange', ax=axs[0])
    axs[0].set_title('Inflation Rate Over Time for Brazil')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Inflation Rate (%)')
    axs[0].tick_params(axis='x', rotation=65)  # Rotate x ticks for Brazil

    # Plotting Inflation for other countries
    sns.lineplot(data=other_inflation, x='date', y='Inflation', hue='country', palette='Set2', ax=axs[1])
    axs[1].set_title('Inflation Rate Over Time for Other Countries')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Inflation Rate (%)')
    axs[1].legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout
    plt.tight_layout()
    plt.show()

    return inflation_data


def unemployment_data():
    unemployment_data = wbdata.get_dataframe({'SL.UEM.TOTL.ZS': 'Unemployment'}, country=countries)
    unemployment_data.reset_index(inplace=True)

    # Convert 'date' column to datetime and filter for 1987–2022
    unemployment_data['date'] = pd.to_datetime(unemployment_data['date'])
    unemployment_data = unemployment_data[(unemployment_data['date'] >= start_date) & (unemployment_data['date'] <= end_date)]

    # Display the Unemployment data
    print("Unemployment Data:")
    print(unemployment_data)

    # Plotting Unemployment data
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=unemployment_data, x='date', y='Unemployment', hue='country')
    plt.title('Unemployment Rate Over Time by Country')
    plt.xlabel('Year')
    plt.ylabel('Unemployment Rate (%)')
    plt.show()
    return unemployment_data



def exchange_rate():
    # Fetch the data
    exchange_rate_data = wbdata.get_dataframe({'PA.NUS.FCRF': 'Exchange Rate'}, country=countries)
    exchange_rate_data.reset_index(inplace=True)
    exchange_rate_data['date'] = pd.to_datetime(exchange_rate_data['date'])
    exchange_rate_data = exchange_rate_data[(exchange_rate_data['date'] >= start_date) & (exchange_rate_data['date'] <= end_date)]
    
    # (Optional) Plotting code here...
    return exchange_rate_data 
    
    # Return the DataFrame
# # Test the function
er_df = exchange_rate()
print("Type of er_df:", type(er_df))


def combine_all(data,inflation_data,exchange_rate_data,gdp_data,unemployment_data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['year'] = data['Date'].dt.year

    gdp_data['date'] = pd.to_datetime(gdp_data['date'])
    gdp_data['year'] = gdp_data['date'].dt.year

    inflation_data['date'] = pd.to_datetime(inflation_data['date'])
    inflation_data['year'] = inflation_data['date'].dt.year

    unemployment_data['date'] = pd.to_datetime(unemployment_data['date'])
    unemployment_data['year'] = unemployment_data['date'].dt.year
    exchange_rate_data['date'] = pd.to_datetime(exchange_rate_data['date'])
    exchange_rate_data['year'] = exchange_rate_data['date'].dt.year

    # Step 2: Merge all datasets based on the 'year' column
    # Start with the main 'data' DataFrame and merge progressively
    combined_data = data.merge(gdp_data[['year', 'GDP']], on='year', how='left')
    combined_data = combined_data.merge(inflation_data[['year', 'Inflation']], on='year', how='left')
    combined_data = combined_data.merge(unemployment_data[['year', 'Unemployment']], on='year', how='left')
    combined_data = combined_data.merge(exchange_rate_data[['year', 'Exchange Rate']], on='year', how='left')

    # Step 3: Sort by 'Date' (not 'year') to ensure forward-filling is done in chronological order
    combined_data = combined_data.sort_values(by='Date')

    # Step 4: Forward-fill missing values for each economic indicator column
    combined_data = combined_data.fillna(method='ffill')

    # Step 5: Drop the extra 'year' column if it's no longer needed
    combined_data = combined_data.drop(columns=['year'], errors='ignore')

    # Step 6: Check the result
    combined_data.head()
    return combined_data




def correlations(combined_data):
    combined_data['Date'] = pd.to_datetime(combined_data['Date'])

    # Calculate correlation with Brent Oil Prices for all indicators
    correlations = {
        'GDP': combined_data['Price'].corr(combined_data['GDP']),
        'Inflation': combined_data['Price'].corr(combined_data['Inflation']),
        'Unemployment': combined_data['Price'].corr(combined_data['Unemployment']),
        'Exchange Rate': combined_data['Price'].corr(combined_data['Exchange Rate'])
    }

    # Display correlation results
    for indicator, corr_value in correlations.items():
        print(f"Correlation between Brent Oil Prices and {indicator}: {corr_value:.2f}")

    # Create a bar plot for the correlations
    plt.figure(figsize=(8, 5))
    sns.barplot(x=list(correlations.keys()), y=list(correlations.values()), palette='coolwarm')
    plt.title('Correlation between Brent Oil Prices and Economic Indicators')
    plt.xlabel('Economic Indicators')
    plt.ylabel('Correlation Coefficient')
    plt.axhline(0, color='grey', linewidth=0.8, linestyle='--')  # Add a line at y=0 for reference
    plt.ylim(-1, 1)  # Set limits for y-axis
    plt.show()

    # Set up the figure for plotting economic indicators
    fig, axs = plt.subplots(5, 1, figsize=(14, 20))  # Create subplots for each indicator

    # Plotting Brent Oil Price
    sns.lineplot(data=combined_data, x='Date', y='Price', color='blue', ax=axs[0])
    axs[0].set_title('Brent Oil Prices Over Time')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Price (USD)')
    axs[0].tick_params(axis='x', rotation=65)

    # Plotting GDP Over Time
    sns.lineplot(data=combined_data, x='Date', y='GDP', color='green', ax=axs[1])
    axs[1].set_title('GDP Over Time')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('GDP (in billions)')
    axs[1].tick_params(axis='x', rotation=65)

    # Plotting Inflation Over Time
    sns.lineplot(data=combined_data, x='Date', y='Inflation', color='orange', ax=axs[2])
    axs[2].set_title('Inflation Over Time')
    axs[2].set_xlabel('Year')
    axs[2].set_ylabel('Inflation Rate (%)')
    axs[2].tick_params(axis='x', rotation=65)

    # Plotting Unemployment Rate Over Time
    sns.lineplot(data=combined_data, x='Date', y='Unemployment', color='red', ax=axs[3])
    axs[3].set_title('Unemployment Rate Over Time')
    axs[3].set_xlabel('Year')
    axs[3].set_ylabel('Unemployment Rate (%)')
    axs[3].tick_params(axis='x', rotation=65)

    # Plotting Exchange Rate Over Time
    sns.lineplot(data=combined_data, x='Date', y='Exchange Rate', color='purple', ax=axs[4])
    axs[4].set_title('Exchange Rate Over Time')
    axs[4].set_xlabel('Year')
    axs[4].set_ylabel('Exchange Rate (to USD)')
    axs[4].tick_params(axis='x', rotation=65)

    # Display plots for economic indicators
    plt.tight_layout()
    plt.show()
