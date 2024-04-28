import pandas as pd

# Load the CSV data into a DataFrame
data = pd.read_csv('D:\Spring 2024\CSE620F\Project Survival of Open Source Libraries\project_code\_-OLD_1_months_interval_data.csv')

# Assuming 'data' is your DataFrame loaded from the CSV
data['period_start'] = pd.to_datetime(data['period_start'])
data['period_end'] = pd.to_datetime(data['period_end'])

# Fill missing numeric values with 0 (assuming that missing means zero)
data.fillna({'forks': 0, 'commits': 0, 'pull_requests': 0, 'issues': 0, 'downloads': 0, 'releases': 0}, inplace=True)

# Convert necessary columns to numeric types
numeric_cols = ['watchers', 'forks', 'stars', 'contributors', 'pull_requests', 'issues', 'downloads', 'releases', 'commits']
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Add a month column for grouping
data['month'] = data['period_start'].dt.to_period('M')

# Specify the aggregation dictionary
aggregations = {col: 'sum' for col in numeric_cols}  # Only sum the numeric columns

# Group by month and apply the aggregation
monthly_activity = data.groupby('month').agg(aggregations)

# Plotting the results
import matplotlib.pyplot as plt

monthly_activity[['commits', 'issues']].plot(kind='line', marker='o')
plt.title('Monthly Development Activity')
plt.xlabel('Month')
plt.ylabel('Total Count')
plt.show()
