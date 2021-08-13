from datetime import date
import requests
import os
import logging
from helper import *


today = date.today()
today = today.strftime(config['date_strftime_format'])
save_path = config['save_path']
retry_count = config['retry_count']


logging.basicConfig(level=config['logging']['level'],
                    filename=config['logging']['file_name'], filemode='a',
                    format=config['logging']['message_format'],
                    datefmt=config['logging']['date_strftime_format'])


console = logging.StreamHandler()
console.setLevel(config["logging_handler"]["level"])
formatter = logging.Formatter(config["logging_handler"]["formatter"])
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class Downloader():

    def __init__(self,urls,download_date):
        self.urls = urls
        self.download_date = download_date

    def start(self,save_path = save_path):
        save_path = save_path + "/" + self.download_date.replace("/","-")
        os.makedirs(save_path,exist_ok=True)
        logging.info("Download Path Created: %s" % save_path)

        download_index = convert_date_to_index(self.download_date)

        for url in self.urls:
            url = url.format(download_index=download_index)
            logging.info("Downloading file from URL: %s" % url)
            filename = url.split('/')[-1].replace(" ", "_")
            file_path = os.path.join(save_path, filename)
            try:
                r = retry_request(url,retry_count)
                if r.ok:
                    if r.headers.get('Content-Type') == 'application/download':
                        logging.info("saving to {}".format(os.path.abspath(file_path)))
                        with open(file_path, 'wb') as f:
                            f.write(r.content)
                    else:  # HTTP status code 4XX/5XX
                        logging.info("Download failed: status code {}\n{}".format(r.status_code, r.headers.get('Content-Type')))
            except:
                logging.exception("Exception: Fail to get {url}".format(url=url))


if __name__ == "__main__":
    history_downloader = Downloader(history_urls,'04/08/2021')
    history_downloader.start()
