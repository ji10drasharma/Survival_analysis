import pandas as pd
import matplotlib.pyplot as plt
import os

# Directory containing CSV files
directory = '/Users/monuchaudhary/Desktop/Survival_analysis/Analysis/metadata'

# Initialize empty lists to store data from each file
all_data = []
file_names = []

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        
        # Read the data from CSV file
        data = pd.read_csv(file_path)
        
        # Append a new column with the filename
        data['language'] = os.path.splitext(filename)[0]
        
        # Append the data and filename to lists
        all_data.append(data)
        # file_names.append(data['filename'])

# Concatenate all data into a single DataFrame
all_data = pd.concat(all_data, ignore_index=True)
all_data.to_csv('/Users/monuchaudhary/Desktop/Survival_analysis/Analysis/metadata.csv', index=False)

# Step 2: Calculate summary statistics
summary_stats = all_data.groupby(['language', 'status'])[['sizeUsers', 'months']].describe()

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
plt.savefig('projects_distribution.eps', format='eps')
plt.savefig('projects_distribution.pdf')

# Step 5: Save summary statistics to a CSV file
summary_stats.to_csv('/Users/monuchaudhary/Desktop/Survival_analysis/Analysis/summary_stats.csv')

# # Display summary statistics and additional insights
# print("Summary Statistics:")
# print(summary_stats)
