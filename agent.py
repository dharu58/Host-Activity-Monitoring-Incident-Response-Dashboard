import psutil
import requests
import time
import socket
import json
from datetime import datetime

API_URL = "http://localhost:8000/api/ingest"
HOST_ID = socket.gethostname()

def collect_metrics():
    # Collect Disk I/O (reads/writes) and Disk Usage
    disk_io = psutil.disk_io_counters()
    disk_usage = psutil.disk_usage('/') # Get usage for the root partition
    
    # Collect Load Averages (1, 5, and 15 minutes)
    load_avg = psutil.getloadavg()
    
    # Collect total process count
    process_count = len(psutil.pids())

    return {
        "host_id": HOST_ID,
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "load_average": { # <--- NEW LOAD AVERAGE
            "1min": load_avg[0],
            "5min": load_avg[1],
            "15min": load_avg[2]
        },
        "process_count": process_count, # <--- NEW PROCESS COUNT
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_recv": psutil.net_io_counters().bytes_recv
        },
        "disk": {
            "usage_percent": disk_usage.percent,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes
        },
        "processes": [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
    }

def main():
    while True:
        metrics = collect_metrics()
        try:
            r = requests.post(API_URL, json=metrics)
            print("Sent:", json.dumps(metrics), "Status:", r.status_code)
        except Exception as e:
            print("Error sending metrics:", e)
        time.sleep(5)

if __name__ == "__main__":
    main()
