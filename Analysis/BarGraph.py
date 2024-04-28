import pandas as pd
import matplotlib.pyplot as plt

all_data = pd.read_csv('/Users/monuchaudhary/Desktop/Survival_analysis/Analysis/all_data_processed.csv')

# Step 2: Calculate summary statistics
summary_stats = all_data.groupby(['language', 'status'])[['sizeUsers', 'lifeSpan','authors','commits','pulls','issues','comments','reviews',]].describe()

# Step 3: Count the number of projects in each status category grouped by filename
status_counts = all_data.groupby(['language', 'status']).size().unstack(fill_value=0)

# Step 4: Normalize the counts to calculate percentages
status_percentages = status_counts.div(status_counts.sum(axis=1), axis=0) * 100

# Step 5: Visualize the distribution of projects by status grouped by filename
# plt.figure(figsize=(10, 6))
status_percentages.plot(kind='bar', stacked=True)
plt.xlabel('Language')
plt.ylabel('Number of Projects')
plt.title('Distribution of Projects by Status (Grouped by Language)')
plt.legend(title='Status')
plt.grid(axis='y')
plt.xticks(range(len(all_data['language'].unique())), all_data['language'].unique(), rotation=45, ha='right')
plt.tight_layout()
# plt.show()

# Step 6: Save the chart as EPS format
plt.savefig('output/projects_distribution.eps', format='eps')
plt.savefig('output/projects_distribution.pdf')

# Step 5: Save summary statistics to a CSV file
summary_stats.to_csv('/Users/monuchaudhary/Desktop/Survival_analysis/Analysis/summary_stats.csv')

# # Display summary statistics and additional insights
# print("Summary Statistics:")
# print(summary_stats)
