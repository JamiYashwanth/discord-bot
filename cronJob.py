import schedule
import time

def job():
    print("I'm working...")

# Schedule the job to run every day at 2:30 PM
schedule.every(). .at("16:04").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
