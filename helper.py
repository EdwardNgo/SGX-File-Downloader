from datetime import datetime,timedelta
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

base_url = "https://links.sgx.com/1.0.0/derivatives-historical/{download_index}/"
tick_link = base_url + "WEBPXTICK_DT.zip"
tick_dat_link = base_url + "TickData_structure.dat"
trade_cancel_link = base_url + "TC.txt"
trade_cancel_dat_link = base_url + "TC_structure.dat"
history_urls = [tick_link,tick_dat_link,trade_cancel_link,trade_cancel_dat_link]

with open('config.json', 'r') as f:
    config = json.load(f)

def is_weekday(date_str):
    """
    input: date_str format "d/m/y" e.g: 1/8/2021
    output: week day or work day
    """
    date_obj = datetime.strptime(date_str,config['date_strftime_format'])
    weekno = date_obj.weekday()
    # weekno = datetime.datetime.today().weekday()
    return True if weekno < 5 else False


def convert_date_to_index(date_str):
    """
    input: date_str format "d/m/y" e.g: 1/8/2021
    output: a number as the index of download path for input date 
    """
    
    date_obj = datetime.strptime(date_str,config['date_strftime_format'])
    dist = date_obj - datetime(2021,8,9)

    if dist.days <= 4 and dist.days >= 0:
        index = 4959 + dist.days

    elif  dist.days >= 7:
        index = 4959 + dist.days - 2*dist.days//7
    
    elif dist.days < 0:
        if abs(dist.days) % 7 != 0:
            index = 4959 + dist.days + 2*(abs(dist.days)//7+1)
        else:
            index = 4959 + dist.days + 2*(abs(dist.days)//7)

    return index


# def convert_index_to_date(idx):
#     """
#     input: index like that one in the web
#     output: date of that index
#     """
    
#     dist = idx - 4959
#     if dist <=4 and dist >=0:
#         idx_date = datetime(2021,8,9) + timedelta(days = dist)
    
#     elif dist >= 5:
#         idx_date = datetime(2021,8,9) + timedelta(days = dist + 2*(dist//7+1))
    
#     elif dist < 0 and dist >= -4:
#         print("Hi")
#         idx_date = datetime(2021,8,9) + timedelta(days = dist - 2*(abs(dist)//5))

#     elif dist <= -5:
#         idx_date = datetime(2021,8,9) + timedelta(days = dist - 2*(abs(dist)//5+1))
    
#     return idx_date.strftime(config['date_strftime_format'])


def retry_request(url,retry = 3):
    session = requests.Session()
    retry = Retry(connect= retry, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    res = session.get(url)
    return res


if __name__ == "__main__":
    print(convert_date_to_index("27/7/2021"))
