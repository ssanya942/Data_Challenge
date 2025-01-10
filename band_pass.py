import pandas as pd
from scipy.signal import butter, filtfilt

# Load the dataset
file_path = 'your/path'
data = pd.read_csv(file_path)

# Define a bandpass filter
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

# Sampling frequency (fs) assumption
fs = 1  # Assuming 1 Hz sampling rate; adjust as necessary

# Apply the bandpass filter to the mean task values
data['TASK_FILTERED'] = bandpass_filter(data['TASK'].fillna(0), lowcut=0.01, highcut=0.1, fs=fs)

# Update TASK_MINUS_BASELINE using the filtered values
data['TASK_MINUS_BASELINE_FILTERED'] = data['TASK_FILTERED'] - data['BASELINE']

# Display the modified DataFrame to the user
