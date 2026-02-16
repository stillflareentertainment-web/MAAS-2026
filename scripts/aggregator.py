import json
import os
import glob
from datetime import datetime

def calculate_daily_pulse():
    # 1. Define paths
    submission_dir = "submissions"
    pulse_file = "community_pulse.json"
    
    # 2. Collect all anonymous .json files from the submissions folder
    # We use *.json to ensure we don't accidentally try to read the .gitkeep file
    submission_files = glob.glob(os.path.join(submission_dir, "*.json"))
    
    if not submission_files:
        print("No new submissions found. Skipping update.")
        return 
    
    total_metrics = {'qs': 0, 'oi': 0, 'ic': 0, 'di': 0, 'ep': 0}
    count = len(submission_files)

    # 3. Process each file
    for file_path in submission_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # We pull the raw slider values (0-100)
                for key in total_metrics:
                    total_metrics[key] += data.get(key, 50)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    # 4. Calculate the new Community Mean
    avg_metrics = {k: round(v / count, 2) for k, v in total_metrics.items()}
    
    # 5. Overwrite the community_pulse.json with fresh data
    output_data = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "averages": avg_metrics,
        "sample_size": count,
        "status": "OS_UPGRADED"
    }

    with open(pulse_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"Successfully aggregated {count} submissions into {pulse_file}.")

    # 6. Cleanup: Remove the processed submissions so they aren't double-counted tomorrow
    for file_path in submission_files:
        os.remove(file_path)
    print("Submissions folder cleared for next cycle.")

if __name__ == "__main__":
    calculate_daily_pulse()
