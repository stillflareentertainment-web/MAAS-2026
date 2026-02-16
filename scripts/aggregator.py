import json
import os
import glob
from datetime import datetime

def calculate_daily_pulse():
    submission_dir = "submissions"
    pulse_file = "community_pulse.json"
    
    # 1. Look for all .json files in the submissions folder
    submission_files = glob.glob(os.path.join(submission_dir, "*.json"))
    
    if not submission_files:
        print("No new data to process today.")
        return 
    
    total_metrics = {'qs': 0, 'oi': 0, 'ic': 0, 'di': 0, 'ep': 0}
    count = len(submission_files)

    # 2. Add up all community numbers
    for file_path in submission_files:
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                for key in total_metrics:
                    total_metrics[key] += data.get(key, 50)
            except:
                continue

    # 3. Calculate the new Averages (The Community Mean)
    avg_metrics = {k: round(v / count, 2) for k, v in total_metrics.items()}
    
    # 4. Overwrite the pulse file with the fresh OS Upgrade
    with open(pulse_file, "w") as f:
        json.dump({
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "averages": avg_metrics,
            "sample_size": count,
            "status": "OS_UPGRADED"
        }, f, indent=2)

    # 5. Clear the inbox for tomorrow
    for file_path in submission_files:
        os.remove(file_path)
    print(f"Successfully processed {count} submissions.")

if __name__ == "__main__":
    calculate_daily_pulse()
