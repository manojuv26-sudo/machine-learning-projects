# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# # Exploratory Data Analysis of AAPL Stock Data

# In this notebook, we will perform an initial exploratory data analysis (EDA) on the downloaded AAPL stock data.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ## 1. Load the data

# Load the CSV file into a pandas DataFrame.
DATA_PATH = 'data/AAPL_stock_data.csv'
df = pd.read_csv(DATA_PATH)

# Display the first 5 rows of the DataFrame.
print("First 5 rows of the data:")
print(df.head())


# ## 2. Data Overview

# Get a summary of the DataFrame, including data types and non-null values.
print("\nData Info:")
df.info()

# Get descriptive statistics for the numerical columns.
print("\nDescriptive Statistics:")
print(df.describe())


# ## 3. Check for Missing Values

# Check if there are any missing values in the dataset.
print("\nMissing Values:")
print(df.isnull().sum())


# ## 4. Visualize the Closing Price

# Let's visualize the closing price of the stock over time to observe its trend.

# Convert the 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Plot the 'Close' price
plt.figure(figsize=(14, 7))
plt.title('AAPL Closing Price (2020-2023)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.plot(df['Close'], label='Close Price')
plt.legend()
plt.grid(True)
# Saving the plot to a file instead of showing it
plt.savefig('data/aapl_closing_price.png')
print("\nPlot of closing price saved to data/aapl_closing_price.png")
