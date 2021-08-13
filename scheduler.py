
import schedule
import time
from file_downloader import Downloader
from datetime import date
from datetime import timedelta
from helper import config,history_urls
import os


def run():
    # Get today's date
    today = date.today()

    # Yesterday date
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime(config["date_strftime_format"])
    history_downloader = Downloader(history_urls,yesterday)
    history_downloader.start()


def check_history_downloader():
    # today = date.today()
    today = date(2021,8,15)
    unavailabe_dir = []
    
    for i in range(2,6):
        week_day = today - timedelta(days=i)
        week_day = week_day.strftime(config["date_strftime_format"]).replace("/","-")

        week_day_dir = os.path.join(config["save_path"],week_day)
        if os.path.exists(week_day_dir):
            if len(os.listdir(week_day_dir)) < config["max_file"]:
                unavailabe_dir.append(week_day.replace("-","/"))
        else:
            os.makedirs(week_day_dir)
            unavailabe_dir.append(week_day.replace("-","/"))

    for day in unavailabe_dir:
        history_downloader = Downloader(history_urls,day)
        history_downloader.start()

schedule.every().tuesday.at("06:00").do(run)
schedule.every().wednesday.at("06:00").do(run)
schedule.every().thursday.at("06:00").do(run)
schedule.every().friday.at("06:00").do(run)
schedule.every().saturday.at("06:00").do(run)
schedule.every().sunday.at("06:00").do(check_history_downloader)

while True:
    schedule.run_pending()
    time.sleep(5)

