import multiprocessing
import time
import random
import os
import psutil

def run_agent_instance(host_id):
    import psutil, requests, socket, json
    from datetime import datetime

    API_URL = "http://localhost:8000/api/ingest"

    while True:
        disk_io = psutil.disk_io_counters()
        disk_usage = psutil.disk_usage('/')
        
        # Collect Load Averages (Note: psutil.getloadavg() may not work on Windows,
        # but we include it for standard Linux/macOS environments, using 0 if unavailable)
        try:
            load_avg = psutil.getloadavg()
        except:
            load_avg = (0, 0, 0)
            
        process_count = len(psutil.pids())

        metrics = {
            "host_id": f"SimHost-{host_id}",
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "load_average": { # NEW
                "1min": load_avg[0],
                "5min": load_avg[1],
                "15min": load_avg[2]
            },
            "process_count": process_count, # NEW
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
        try:
            r = requests.post(API_URL, json=metrics)
            print(f"Host {host_id} sent metrics, status {r.status_code}")
        except Exception as e:
            print(f"Host {host_id} error:", e)
        time.sleep(random.randint(3, 7))

if __name__ == "__main__":
    num_hosts = 3
    processes = []
    for i in range(num_hosts):
        p = multiprocessing.Process(target=run_agent_instance, args=(i,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
