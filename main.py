import requests
import json
import time
import os
from lxml import etree
from rich import print
from typing import List

output_file = "dlist.txt"
config_file = "config.json"
config_file = open(config_file, "r+")
config = json.load(config_file)


class RSSReader():
    max_item_size = 5

    def __init__(self, config):
        self.config = config

    def export_download_link(self) -> List[str]:
        rss_list = self.config["source"]
        for rssitem in rss_list:
            rss_text = requests.get(rssitem["link"]).text
            selector = etree.fromstring(rss_text)
            for one in selector.xpath(
                    "//rss/channel/item/link/text()")[:self.max_item_size]:
                yield one


class ConfigLogger():
    log_size = 100

    def __init__(self, config, config_file):
        self.config = config
        self.__config_file = config_file

    def filter(self, links) -> List[str]:
        history = config["log"]
        return list(filter(lambda x: x not in history, links))

    def log(self, links: List[str]) -> bool:
        log = links + config["log"]
        config["log"] = log[:self.log_size]
        config_file.seek(0)
        config_file.truncate()
        config_file.write(json.dumps(config, indent=4))
        return True

def main():
    rss = RSSReader(config)
    logger = ConfigLogger(config, config_file)
    links = list(rss.export_download_link())
    links = logger.filter(links)
    if len(links) == 0:
        print("Current queue is empty.")
        return
    print(":tada:", f"{len(links)} file need to download, Start generate download manifest file.")
    open(output_file, "w+").write('\n'.join(links))
    logger.log(links)
    exit(1)


if __name__ == "__main__":
    count = 60
    while count > 0:
        main()
        time.sleep(60 * 1000)
        count -= 1
    
