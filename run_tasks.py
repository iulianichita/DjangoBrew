import schedule
import time
import django
import os
import sys
from aplicatie_ex import tasks
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proiect1.settings')
django.setup()

def run_scheduler():
    
    schedule.every(10).minutes.do(tasks.stergeusers_mailneconfirmat)
    
    schedule.every().tuesday.at("10:00").do(tasks.sendemail_tousers)
    
    schedule.every(4320).minutes.do(tasks.newusers_email) # fiecare 3 zile
    
    schedule.every().tuesday.at("12:00").do(tasks.most_viewed_lastweek)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("Scheduler oprit manual.")
        sys.exit()
        
        