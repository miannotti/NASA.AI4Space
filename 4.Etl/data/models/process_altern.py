import os
import pandas as pd
import numpy as np
from obspy import read
import xgboost as xgb
import joblib  # To load your pre-trained XGBoost model
from scipy.ndimage import uniform_filter1d  # For simple moving average
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Progress bar for tracking progress


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


# Function to group data by minute without averaging the prediction
def group_data_by_minute(df):
    df['timestamp'] = pd.to_datetime(df['second'], unit='s')  # Convert seconds to timestamp

    # Group by minute
    df['minute'] = df['timestamp'].dt.floor('T')  # Round down to the nearest minute
    grouped = df.groupby('minute').agg({
        'original_velocity': 'mean',  # Use mean of original velocity for each minute
        'filtered_velocity': 'mean',  # Use mean of filtered velocity for each minute
        'prediction': lambda x: 1 if (x == 1).any() else 0  # If any second in the minute has a 1, set prediction to 1, else 0
    }).reset_index()

    return grouped


# Function to export grouped data to JSON
def export_to_json(df, output_file):
    json_data = df.to_json(orient='records', date_format='iso')
    with open(output_file, 'w') as f:
        f.write(json_data)
    print(f"Data exported to {output_file}")


# Function to process a single mseed file and output results
def process_single_day(mseed_file, model, output_dir):
    try:
        # Generate predictions for the day
        day_predictions = generate_predictions_for_day(model, mseed_file)

        # Group data by minute
        grouped_data = group_data_by_minute(day_predictions)

        # Create output file paths
        base_filename = os.path.basename(mseed_file).replace('.mseed', '')
        output_csv = os.path.join(output_dir, f'{base_filename}_grouped.csv')
        output_json = os.path.join(output_dir, f'{base_filename}_grouped.json')

        # Save the grouped data to a CSV file
        grouped_data.to_csv(output_csv, index=False)

        # Export to JSON
        export_to_json(grouped_data, output_json)

        return f"Processed {mseed_file}"
    except Exception as e:
        return f"Error processing {mseed_file}: {e}"


# Function to process all .mseed files in a directory using multiple threads
def process_all_mseed_files(mseed_dir, model, output_dir, max_workers=4):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Find all .mseed files in the directory
    mseed_files = [os.path.join(mseed_dir, file) for file in os.listdir(mseed_dir) if file.endswith('.mseed')]

    # Initialize progress bar
    with tqdm(total=len(mseed_files), desc="Processing .mseed files") as pbar:
        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit tasks for each .mseed file
            futures = [executor.submit(process_single_day, mseed_file, model, output_dir) for mseed_file in mseed_files]

            # Process results as they complete
            for future in as_completed(futures):
                result = future.result()
                print(result)
                pbar.update(1)


# Example usage to process all .mseed files:
mseed_dir = r'/4.Etl/data/moon/test/data/S12_GradeB'  # Replace with your directory containing .mseed files
output_dir = r'/4.Etl/data/output_files_model/moon/S12_GradeB'  # Replace with your desired output directory

# Load the pre-trained XGBoost model from file (replace 'xgb_model.pkl' with the actual path to your model)
xgb_model = joblib.load('xgb_model.pkl')

# Process all .mseed files using 4 threads
process_all_mseed_files(mseed_dir, xgb_model, output_dir, max_workers=1)
