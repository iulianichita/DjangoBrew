import schedule
import time

def f():
    print("Se va afisa la fiecare minut")

schedule.every(1).minute.do(f)

while True:
    schedule.run_pending()
    time.sleep(1)
    
