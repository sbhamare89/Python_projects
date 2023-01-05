import download
import time, schedule

def job():
    print("Updating CSV's for today...")
    download.NseIndia()

schedule.every().day.at("16:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)