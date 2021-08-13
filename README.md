# SGX-File-Downloader

## Description


Design a job to download the following files daily from the above website.

* WEBPXTICK_DT-*.zip

* TickData_structure.dat

*  TC_*.txt

* TC_structure.dat

## How to run
* Clone this repo and make sure you've installed python
* Install python package 

```
pip install -r requirements.txt
```

* Change the config as you want at "config.json"
* To run for a specific day:

```python3
python main.py 09/8/2021
```

* To schedule daily:
```python3
python scheduler.py
```
## Solution

### File Downloader

I found the links to download the following files had a structure like:

https://links.sgx.com/1.0.0/derivatives-historical/{download_index}/ + required file


The download_index is increment by day and I write a function with input as date and output is the download_index which means I can map a date to download_index.
  
With this link templates, I can download not only current data but historical also. I use python with requests library to download file simply and make use of its feature like retry.

The "file_downloader.py" contains code for downloading the required files. The downloaded file will be saved into a child folder with the name is date and the parent folder is set by the config file
  

The "helper.py" contains some functions for converting date to index which I mentioned above


The "main.py" contains code for running the downloader with specific date with format: "d/m/Y"

```python3

python main.py 09/8/2021

```

### Scheduler

The downloader will start daily at 6 AM from tuesday to saturday because it will get the yesterday data.

The reason why for that is we don't know when the data today comes and I come up with that today will download yesterday data. In case we want to get today's data without doing like me, I recommend we set job to start at 2 points of time in day at late night.

Another job in the scheduler is the check fail file job. It will run on every Sunday to check if data is missing that week.

### Config file

The config file is written with json format "config.json". It contains several configs like logging ( What should be written on file or show on terminal ), save path of the downloaded file, max retry for the request

## Challenge

### About the recovering plan
For automatic redownloading, I write a job that run on every Sunday to check if the data is ok for every day in that week so there is a way for recovering plan. However this method can not make sure that it run well because it can be failed at any time like the download job everyday so this somehow reduce the failed rate.

For manually check failed download, if we have a small amount like this I think it should be considered. I recommend Airflow with UI instead of the scheduler like this so that we can do the manually check easier.

I recommend using both automatic and manual method for recovering plan

### Some problems not mentioned in the test requirements

After doing this mini project I asked myself some problems

* In this case, I found data only on week day not weekend. What if in the future there will be data on weekend -> have some modified on my code about date mapping to download_index and scheduler (Not complicated)

* As I mentioned above the auto redownload missed file is ran for every week but it can be failed due to some factors like networking down, ... for my recommendation, the manual check and auto redownload can be implemented together with some orchestration platform like Airflow.

