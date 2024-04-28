import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Load data
data = pd.read_csv('D:\Spring 2024\CSE620F\Project Survival of Open Source Libraries\project_code\_-OLD_1_months_interval_data.csv', parse_dates=['period_start', 'period_end'])

# Set 'period_start' as the index for time series analysis
data.set_index('period_start', inplace=True)

# Define numeric columns and ensure they are treated as numeric in case they have non-numeric values or are missing
numeric_cols = ['commits', 'issues', 'contributors', 'pull_requests', 'downloads', 'releases']  # Assuming all these columns are numeric
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

# Resample data monthly and sum up the metrics
monthly_data = data[numeric_cols].resample('M').sum()

# Check if there are at least 12 months of data to calculate a 12-month rolling average
if len(monthly_data) >= 12:
    monthly_data['commits_ma'] = monthly_data['commits'].rolling(window=12).mean()
    monthly_data['issues_ma'] = monthly_data['issues'].rolling(window=12).mean()
else:
    print("Not enough data to calculate a 12-month rolling average.")

# Plotting the rolling averages, check if moving averages were calculated
if 'commits_ma' in monthly_data.columns:
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    monthly_data['commits_ma'].plot(ax=ax[0], title='12-Month Rolling Mean of Commits')
    ax[0].set_ylabel('Average Commits')
    monthly_data['issues_ma'].plot(ax=ax[1], title='12-Month Rolling Mean of Issues')
    ax[1].set_ylabel('Average Issues')
    plt.tight_layout()
    plt.show()

# Check if there is enough data to perform autocorrelation and partial autocorrelation plots
if len(monthly_data) > 24:
    plot_acf(monthly_data['commits'].dropna(), lags=24, title='Autocorrelation of Commits')
    plt.show()
    plot_pacf(monthly_data['commits'].dropna(), lags=24, title='Partial Autocorrelation of Commits')
    plt.show()
else:
    print("Not enough data for 24 lags in ACF and PACF plots.")
