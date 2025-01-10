import pandas as pd
from scipy.stats import ttest_rel
import matplotlib.pyplot as plt
import mne
import numpy as np

# Load the dataset
data = pd.read_csv('/Users/sanya/Downloads/DataChallenge2024_forStudents (1)/data/MainTask/SPNDataChallenge_columns.csv')

# Map SESSION to expertise levels
data['EXPERTISE'] = data['SESSION'].map({1: 'Consultant', 2: 'Registrar', 3: 'Novice'})

# Define channel mapping based on optode positioning
channel_mapping = {
    1: 'Fp1', 2: 'Fp2', 3: 'F7', 4: 'F8', 5: 'AF3', 6: 'AF4', 7: 'FC5', 8: 'FC6',
    9: 'T7', 10: 'T8', 11: 'P7', 12: 'P8', 13: 'F3', 14: 'F4', 15: 'C3', 16: 'C4',
    17: 'CP5', 18: 'CP6', 19: 'P3', 20: 'P4', 21: 'O1', 22: 'O2', 23: 'Oz', 24: 'Cz'
}

# Check for missing data or unequal distribution of channels
def check_channel_coverage(data):
    for expertise in ['Consultant', 'Registrar', 'Novice']:
        subset = data[data['EXPERTISE'] == expertise]
        channel_counts = subset['CHANNEL'].value_counts().sort_index()
        print(f"Channel counts for {expertise}:")
        print(channel_counts)
        print()

# Function to perform paired t-test for lateralization
def t_test_lateralization(data):
    for expertise in ['Consultant', 'Registrar', 'Novice']:
        subset = data[data['EXPERTISE'] == expertise]

        if subset.empty:
            print(f"No valid data for {expertise} to analyze lateralization.")
            continue

        # Separate Left and Right Hemisphere Channels
        left_channels = subset.loc[subset['CHANNEL'] >= 13, 'TASK_MINUS_BASELINE'].reset_index(drop=True)
        right_channels = subset.loc[subset['CHANNEL'] <= 12, 'TASK_MINUS_BASELINE'].reset_index(drop=True)

        # Ensure both hemispheres have equal-length data
        min_length = min(len(left_channels), len(right_channels))
        left_channels = left_channels[:min_length]
        right_channels = right_channels[:min_length]

        if left_channels.empty or right_channels.empty:
            print(f"Insufficient data for {expertise} to perform t-test.")
            continue

        # Perform paired t-test
        t_stat, p_value = ttest_rel(left_channels, right_channels)

        # Calculate Lateralization Index
        left_mean = left_channels.mean()
        right_mean = right_channels.mean()
        lateralization_index = (right_mean - left_mean) / (right_mean + left_mean)

        # Print results
        print(f"T-Test Results for {expertise}:")
        print(f"T-Statistic: {t_stat}, P-Value: {p_value}")
        print(f"Lateralization Index: {lateralization_index}")
        if p_value < 0.05:
            print(f"Conclusion: The activity is significantly lateralized for {expertise}.")
        else:
            print(f"Conclusion: The activity is not significantly lateralized for {expertise}.")
        print()

# Function to perform paired t-test for orbital vs. lateral activity in novices
def t_test_orbital_vs_lateral(data):
    subset = data[data['EXPERTISE'] == 'Novice']

    if subset.empty:
        print("No valid data for Novice to analyze orbital vs. lateral activity.")
        return

    # Define Orbital and Lateral Channels
    orbital_channels = subset.loc[subset['CHANNEL'].isin([1, 2, 3, 4, 13, 14, 15, 16]), 'TASK_MINUS_BASELINE'].reset_index(drop=True)
    lateral_channels = subset.loc[subset['CHANNEL'].isin([5, 6, 7, 8, 9, 10, 11, 12, 17, 18, 19, 20, 21, 23, 24]), 'TASK_MINUS_BASELINE'].reset_index(drop=True)

    # Ensure both groups have equal-length data
    min_length = min(len(orbital_channels), len(lateral_channels))
    orbital_channels = orbital_channels[:min_length]
    lateral_channels = lateral_channels[:min_length]

    if orbital_channels.empty or lateral_channels.empty:
        print("Insufficient data to perform t-test for orbital vs. lateral activity in novices.")
        return

    # Perform paired t-test
    t_stat, p_value = ttest_rel(orbital_channels, lateral_channels)

    # Calculate Orbital vs. Lateral Index
    orbital_mean = orbital_channels.mean()
    lateral_mean = lateral_channels.mean()
    orbital_lateral_index = (orbital_mean - lateral_mean) / (orbital_mean + lateral_mean)

    # Print results
    print("T-Test Results for Orbital vs. Lateral Activity in Novices:")
    print(f"T-Statistic: {t_stat}, P-Value: {p_value}")
    print(f"Orbital vs. Lateral Index: {orbital_lateral_index}")
    print(f"Orbital Mean: {orbital_mean}, Lateral Mean: {lateral_mean}")
    if p_value < 0.05:
        print("Conclusion: Orbital activity is significantly higher than lateral activity in novices.")
    else:
        print("Conclusion: There is no significant difference between orbital and lateral activity in novices.")
    print()

    # Visualization of Orbital vs Lateral Activity
    plt.bar(['Orbital', 'Lateral'], [orbital_mean, lateral_mean], color=['blue', 'red'])
    plt.title("Orbital vs Lateral Activity in Novices")
    plt.ylabel("Mean Task Minus Baseline")
    plt.show()

# Function to create a topographical brain map using MNE
def plot_topographical_map(data, expertise):
    subset = data[data['EXPERTISE'] == expertise]
    if subset.empty:
        print(f"No data available for {expertise} to plot topographical map.")
        return

    # Map channel indices to standard 10-20 channel names
    subset = subset.copy()
    subset['Mapped_Channel'] = subset['CHANNEL'].map(channel_mapping)
    valid_channels = subset.dropna(subset=['Mapped_Channel'])

    # Create synthetic info and data
    info = mne.create_info(
        ch_names=valid_channels['Mapped_Channel'].unique().tolist(),
        sfreq=1,
        ch_types="eeg"
    )

    # Map channels to their activity values
    activity = valid_channels.groupby('Mapped_Channel')['TASK_MINUS_BASELINE'].mean()
    data_array = np.zeros(len(info['ch_names']))
    for idx, ch in enumerate(info['ch_names']):
        if ch in activity.index:
            data_array[idx] = activity[ch]

    # Create MNE Evoked object for topography
    evoked = mne.EvokedArray(data_array[:, np.newaxis], info, tmin=0)
    evoked.set_montage('standard_1020')

    # Plot topography
    evoked.plot_topomap(times=[0], scalings=1, time_format="")

# Check channel coverage for completeness
check_channel_coverage(data)

# Run the t-test for lateralization
t_test_lateralization(data)

# Run the t-test for orbital vs. lateral activity in novices
t_test_orbital_vs_lateral(data)

# Plot topographical maps for each expertise
for exp in ['Consultant', 'Registrar', 'Novice']:
    plot_topographical_map(data, exp)
