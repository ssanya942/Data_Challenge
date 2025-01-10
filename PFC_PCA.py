import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('/Users/sanya/Downloads/DataChallenge2024_forStudents (1)/data/MainTask/SPNDataChallenge_columns.csv')

# Map SESSION to expertise levels
data['EXPERTISE'] = data['SESSION'].map({1: 'Consultant', 2: 'Registrar', 3: 'Novice'})

# Select columns for PCA analysis
columns_for_pca = ['TASK_MINUS_BASELINE', 'AREA_UNDER_CURVE_TASK', 'STD_TASK']
data_pca = data.dropna(subset=columns_for_pca)

# Center the data (skip standardization)
data_centered = data_pca[columns_for_pca] - data_pca[columns_for_pca].mean()
data_std = data_centered  # Skip division by standard deviation

# Perform PCA manually
cov_matrix = np.cov(data_std.T)
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# Project the data onto the first two principal components
projected_data = np.dot(data_std, eigenvectors[:, :2])
projected_data[:, 0] *= eigenvalues[0]  # Scale by the first eigenvalue
projected_data[:, 1] *= eigenvalues[1]  # Scale by the second eigenvalue

data_pca['Component 1'] = projected_data[:, 0]
data_pca['Component 2'] = projected_data[:, 1]

# Plot PCA results
plt.figure(figsize=(12, 8))
for expertise, marker, color in zip(['Novice', 'Registrar', 'Consultant'], ['+', 's', '^'], ['red', 'green', 'blue']):
    subset = data_pca[data_pca['EXPERTISE'] == expertise]
    plt.scatter(subset['Component 1'], subset['Component 2'], marker=marker, color=color, label=expertise, alpha=0.6)

plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.axvline(0, color='black', linestyle='--', linewidth=1)
plt.title('PCA Analysis of Prefrontal Cortex Activation Across Expertise Levels')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.legend(title='Expertise Levels')
plt.grid(True)
plt.show()
