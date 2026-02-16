import json
import os
import glob
from datetime import datetime

def calculate_daily_pulse():
    submission_dir = "submissions"
    pulse_file = "community_pulse.json"
    
    # 1. Collect all anonymous submissions
    submission_files = glob.glob(os.path.join(submission_dir, "*.json"))
    data_files = [f for f in submission_files if not f.endswith('.gitkeep')]
    
    if not data_files:
        print("No new data today. Keeping current pulse.")
        return 
    
    total_metrics = {'qs': 0, 'oi': 0, 'ic': 0, 'di': 0, 'ep': 0}
    count = 0

    # 2. Add up all community inputs
    for file_path in data_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for key in total_metrics:
                    total_metrics[key] += data.get(key, 50)
                count += 1
        except:
            continue

    if count == 0: return

    # 3. Calculate the New Community Mean
    avg_metrics = {k: round(v / count, 2) for k, v in total_metrics.items()}
    
    # 4. Save to the main keeper file
    output_data = {
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "averages": avg_metrics,
        "sample_size": count,
        "status": "OS_UPGRADED"
    }

    with open(pulse_file, "w") as f:
        json.dump(output_data, f, indent=2)

    # 5. Clear the inbox
    for file_path in data_files:
        os.remove(file_path)
    print(f"OS UPGRADED using {count} inputs.")

if __name__ == "__main__":
    calculate_daily_pulse()
