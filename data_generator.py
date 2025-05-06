import csv
import random
from datetime import datetime, timedelta

def generate_data(num_servers=10, hours=24*7):
    headers = ['server_id', 'metric_name', 'metric_value', 'timestamp']
    with open('telemetry.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        now = datetime.now()
        for server in range(num_servers):
            server_id = f"server_{server:02d}"
            for hour in range(hours):
                timestamp = now - timedelta(hours=hour)
                # Generate CPU data
                writer.writerow([
                    server_id,
                    'cpu',
                    random.uniform(0, 100),
                    timestamp.isoformat()
                ])
                # Generate Memory data
                writer.writerow([
                    server_id,
                    'memory',
                    random.uniform(0, 100),
                    timestamp.isoformat()
                ])
                # Generate Disk data
                writer.writerow([
                    server_id,
                    'disk',
                    random.uniform(0, 100),
                    timestamp.isoformat()
                ])

if __name__ == "__main__":
    generate_data()