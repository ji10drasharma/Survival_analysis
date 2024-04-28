import matplotlib.pyplot as plt

# Given data
data = {
    ('Laravel', 'Alive'): {'mean': 2.372093023255814, 'std': 0.6554989308027126},
    ('Laravel', 'Dead'): {'mean': 1.4310344827586208, 'std': 0.5654394026669208},
    ('Laravel', 'Zombie'): {'mean': 2.7142857142857144, 'std': 0.4879500364742666},
    ('NPM', 'Alive'): {'mean': 2.5813953488372094, 'std': 0.5834001004067302},
    ('NPM', 'Dead'): {'mean': 1.7619047619047619, 'std': 0.6615814157039656},
    ('NPM', 'Zombie'): {'mean': 2.6, 'std': 0.5477225575051661},
    ('R', 'Alive'): {'mean': 2.2650602409638556, 'std': 0.7503549948377701},
    ('R', 'Dead'): {'mean': 1.6020408163265305, 'std': 0.5874950478995914},
    ('R', 'Zombie'): {'mean': 2.4444444444444446, 'std': 0.6156987634551992},
    ('WordPress', 'Alive'): {'mean': 2.4782608695652173, 'std': 0.6899905481394213},
    ('WordPress', 'Dead'): {'mean': 1.4722222222222223, 'std': 0.6794275450111211},
    ('WordPress', 'Zombie'): {'mean': 2.736842105263158, 'std': 0.6533762964749499},
}

# Convert data to lists for boxplot
box_data = {status: [data.get((project, status), {'mean': 0})['mean'] for project in sorted(set([key[0] for key in data.keys()]))] for status in sorted(set([key[1] for key in data.keys()]))}

print(box_data)

# Plot box plot
plt.figure(figsize=(10, 6))
plt.boxplot([box_data[status] for status in box_data.keys()], labels=box_data.keys(), patch_artist=True)

plt.xlabel('Status')
plt.ylabel('Mean Users Size')
plt.title('Box Plot of Mean User Size by Status')

plt.tight_layout()
# plt.show()

plt.savefig('BoxPlotByStatusForAllProjects.eps', format='eps')
plt.savefig('BoxPlotByStatusForAllProjects.pdf')
