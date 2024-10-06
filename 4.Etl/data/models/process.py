import os
import joblib
import pandas as pd
import numpy as np
from obspy import read, UTCDateTime
import xgboost as xgb
from scipy.ndimage import uniform_filter1d  # For simple moving average
import json
from concurrent.futures import ThreadPoolExecutor, as_completed  # For multi-threading
from tqdm import tqdm  # Progress bar


# Function to filter the data with a narrower bandwidth
def bandpass_filter(tr, freqmin=0.8, freqmax=0.9):  # Adjusted bandwidth
    return tr.filter('bandpass', freqmin=freqmin, freqmax=freqmax)


# Function to calculate features from a window
def calculate_features(window_data):
    return {
        "velocity_mean": np.mean(window_data),
        "velocity_std": np.std(window_data),
        "velocity_max": np.max(window_data),
        "velocity_min": np.min(window_data),
        "velocity_variance": np.var(window_data)
    }


# Function to generate predictions for a single day (file) using the XGBoost model
def generate_predictions_for_day(model, mseed_file, window_size=60, freqmin=0.8, freqmax=0.9):
    data = []

    # Load the mseed file and filter it
    st = read(mseed_file)
    st_filtered = bandpass_filter(st[0], freqmin=freqmin, freqmax=freqmax)

    # Get the original and filtered velocities
    original_velocity = st[0].data
    filtered_velocity = st_filtered.data

    # Loop through the data and make predictions starting from the 60th second
    for i in range(len(original_velocity) - window_size):
        # Extract a sliding window of data (last 60 seconds)
        window_data = filtered_velocity[i:i + window_size]
        features = calculate_features(window_data)

        # Use the model to predict if there's an event (1) or no event (0)
        feature_array = np.array(
            [features["velocity_mean"], features["velocity_std"], features["velocity_max"], features["velocity_min"],
             features["velocity_variance"]]).reshape(1, -1)
        prediction = model.predict(feature_array)[0]

        # Store the results
        data.append({
            "second": i + window_size,  # We start predicting after 60 seconds
            "original_velocity": original_velocity[i + window_size],
            "filtered_velocity": filtered_velocity[i + window_size],
            "prediction": prediction
        })

    return pd.DataFrame(data)


# Function to apply moving average using uniform_filter1d from scipy.ndimage
def apply_moving_average(df, window_size=60):
    df['smoothed_original_velocity'] = uniform_filter1d(df['original_velocity'], size=window_size)
    df['smoothed_filtered_velocity'] = uniform_filter1d(df['filtered_velocity'], size=window_size)
    df['smoothed_prediction'] = uniform_filter1d(df['prediction'], size=window_size)  # Smoothing the prediction
    return df


# Function to export grouped data to JSON
def export_to_json(df, output_file):
    json_data = df.to_json(orient='records', date_format='iso')
    with open(output_file, 'w') as f:
        f.write(json_data)
    print(f"Data exported to {output_file}")


# Function to process a single mseed file and output results for the frontend
def process_single_day(mseed_file, model, output_csv=None, output_json=None):
    # Generate predictions for the day
    day_predictions = generate_predictions_for_day(model, mseed_file)

    # Apply moving average smoothing to the predictions
    smoothed_predictions = apply_moving_average(day_predictions)

    # Save the smoothed predictions to a CSV file if output_csv is provided
    if output_csv:
        smoothed_predictions.to_csv(output_csv, index=False)
        print(f"Smoothed predictions for the day saved to {output_csv}")

    # Export to JSON if output_json is provided
    if output_json:
        export_to_json(smoothed_predictions, output_json)


# Function to process all .mseed files in a directory using multiple threads
def process_all_mseed_files(directory, model, num_threads=4):
    # Find all .mseed files in the directory
    mseed_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mseed')]

    # Use a thread pool to process files concurrently
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        print(f"Processing {len(mseed_files)} files with {num_threads} threads...")

        # Use tqdm to track progress
        with tqdm(total=len(mseed_files)) as pbar:
            for mseed_file in mseed_files:
                output_csv = f"{os.path.splitext(mseed_file)[0]}_predictions.csv"
                output_json = f"{os.path.splitext(mseed_file)[0]}_predictions.json"
                # Submit the processing of each file to the thread pool
                futures.append(executor.submit(process_single_day, mseed_file, model, output_csv, output_json))

            # As each file is completed, update the progress bar
            for future in as_completed(futures):
                pbar.update(1)

    print("All files processed.")


# Example usage for processing all .mseed files in a directory:
mseed_directory = r'D:\NASA\2024\app\data\mars\test\data'  # Replace with the actual path to your directory
xgb_model = joblib.load('xgb_model.pkl')  # Load the pre-trained XGBoost model

# Process all .mseed files using 4 threads
process_all_mseed_files(mseed_directory, xgb_model, num_threads=1)
