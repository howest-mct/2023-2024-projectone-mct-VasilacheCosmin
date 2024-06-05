from datetime import date, datetime
import time

# Huidige timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
timestamp2 = time.time()
print("Timestamp:", timestamp)
print("Timestamp2:", timestamp2)



today_start = datetime.combine(date.today(), datetime.min.time())
today_end = datetime.combine(date.today(), datetime.max.time())

print(today_start)
print(today_end)