from file_downloader import Downloader
import sys
from datetime import date,timedelta
from helper import is_weekday, history_urls,config
import json

with open('config.json', 'r') as f:
    config = json.load(f)


def get_user_input():

    if len(sys.argv) > 1:
        download_date = sys.argv[1]
    else:
        # Get today's date
        today = date.today()
        #set default date as today's date
        download_date = str(today.strftime(config["date_strftime_format"]))

    return download_date


if __name__ == '__main__':
    download_date = get_user_input()

    if is_weekday(download_date):
        history_downloader = Downloader(history_urls,download_date)
        # history_downloader = Downloader(history_urls,download_date)
        history_downloader.start()
    else:
        print("This is weekend and data is not available")

