from datetime import datetime
import time

# Huidige timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
timestamp2 = time.time()
print("Timestamp:", timestamp)
print("Timestamp2:", timestamp2)