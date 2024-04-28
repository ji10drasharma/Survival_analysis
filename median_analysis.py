import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset into a DataFrame
data = pd.read_csv('your_dataset.csv')

# Calculate the total number of commits for each project
total_commits_per_project = data.groupby('repo_name')['commits'].sum()

# Compute the median number of commits across all projects
median_commits = total_commits_per_project.median()

# Plot a histogram of commits per project
plt.figure(figsize=(10, 6))
plt.hist(total_commits_per_project, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(median_commits, color='red', linestyle='dashed', linewidth=1, label=f'Median: {median_commits:.2f}')
plt.xlabel('Total Commits')
plt.ylabel('Frequency')
plt.title('Distribution of Commits per Project')
plt.legend()
plt.grid(True)
plt.show()

# Determine which projects have more commits than the median
projects_above_median = total_commits_per_project[total_commits_per_project > median_commits]

# Count the number of projects that do not have more commits than the median
projects_below_median = total_commits_per_project[total_commits_per_project <= median_commits]

# Display the results
print("Number of projects with more commits than the median:", len(projects_above_median))
print("Number of projects with fewer commits than or equal to the median:", len(projects_below_median))
