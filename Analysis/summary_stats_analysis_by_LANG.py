import pandas as pd
import matplotlib.pyplot as plt

# Provided data
data = {
    ('Laravel', 'Alive'): {'count': 43, 'mean': 2.372093023255814, 'std': 0.6554989308027126, 'min': 1, '25%': 2, '50%': 2, '75%': 3, 'max': 3},
    ('Laravel', 'Dead'): {'count': 58, 'mean': 1.4310344827586208, 'std': 0.5654394026669208, 'min': 1, '25%': 1, '50%': 1, '75%': 2, 'max': 3},
    ('Laravel', 'Zombie'): {'count': 7, 'mean': 2.7142857142857144, 'std': 0.4879500364742666, 'min': 2, '25%': 2.5, '50%': 3, '75%': 3, 'max': 3},
    ('NPM', 'Alive'): {'count': 86, 'mean': 2.5813953488372094, 'std': 0.5834001004067302, 'min': 1, '25%': 2, '50%': 3, '75%': 3, 'max': 3},
    ('NPM', 'Dead'): {'count': 189, 'mean': 1.7619047619047619, 'std': 0.6615814157039656, 'min': 1, '25%': 1, '50%': 2, '75%': 2, 'max': 3},
    ('NPM', 'Zombie'): {'count': 5, 'mean': 2.6, 'std': 0.5477225575051661, 'min': 2, '25%': 2, '50%': 3, '75%': 3, 'max': 3},
    ('R', 'Alive'): {'count': 83, 'mean': 2.2650602409638556, 'std': 0.7503549948377701, 'min': 1, '25%': 2, '50%': 2, '75%': 3, 'max': 3},
    ('R', 'Dead'): {'count': 98, 'mean': 1.6020408163265305, 'std': 0.5874950478995914, 'min': 1, '25%': 1, '50%': 2, '75%': 2, 'max': 3},
    ('R', 'Zombie'): {'count': 18, 'mean': 2.4444444444444446, 'std': 0.6156987634551992, 'min': 1, '25%': 2, '50%': 2.5, '75%': 3, 'max': 3},
    ('WordPress', 'Alive'): {'count': 161, 'mean': 2.4782608695652173, 'std': 0.6899905481394213, 'min': 1, '25%': 2, '50%': 3, '75%': 3, 'max': 3},
    ('WordPress', 'Dead'): {'count': 360, 'mean': 1.4722222222222223, 'std': 0.6794275450111211, 'min': 1, '25%': 1, '50%': 1, '75%': 2, 'max': 3},
    ('WordPress', 'Zombie'): {'count': 19, 'mean': 2.736842105263158, 'std': 0.6533762964749499, 'min': 1, '25%': 3, '50%': 3, '75%': 3, 'max': 3},
}

# Convert data to DataFrame
df = pd.DataFrame.from_dict(data, orient='index').reset_index()
df.rename(columns={'level_0': 'Language', 'level_1': 'Status'}, inplace=True)

# Plot box plot
plt.figure(figsize=(10, 6))
boxprops = dict(linestyle='-', linewidth=2, color='black')
medianprops = dict(linestyle='-', linewidth=2, color='firebrick')
whiskerprops = dict(linestyle='--', linewidth=2, color='black')
capprops = dict(linestyle='-', linewidth=2, color='black')
df.boxplot(column='mean', by='Language', grid=False, showfliers=False,
           boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops)
plt.xlabel('Language')
plt.ylabel('Mean')
plt.title('Box Plot of User Size Mean for Different Languages')

plt.tight_layout()
plt.show()
