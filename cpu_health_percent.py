
import time
import psutil


CPU_THRESHOLD = 80  

print("Monitoring CPU usage...")

while True:
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > CPU_THRESHOLD:
            print(f"Alert! CPU usage exceeds threshold: {cpu_usage}%")
        # (Optional) slow down monitoring slightly
        time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        break

    except Exception as e:
        print(f"An error occurred: {e}")
        break
