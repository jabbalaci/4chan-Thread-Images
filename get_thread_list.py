#!/usr/bin/env python3

"""
Extract images (PNGs and JPGs) from a 4chan thread.

A thread's URL looks like this (sample): https://boards.4channel.org/w/thread/2159787

Usage:

    $ ./get_thread_list.py <4chan_thread_url>

The image list will be saved to a file called `down.txt`.
Copy `down.txt` to a folder and issue the following command:

    $ wget -i down.txt

to download all the images.

GitHub: https://github.com/jabbalaci/4chan-Thread-Images
Author: Laszlo Szathmary, 2020, jabba.laci@gmail.com
"""

import json
import os
import sys
from pprint import pprint

import requests

import mylogging as log

JSON_FILE = "index.json"
CDN_BASE_URL = "https://is2.4chan.org"  # you might have to update it


class Downloader:
    def __init__(self, thread_url):
        self.thread_url = thread_url
        self.board_id = thread_url.split("/")[3]
        log.info(f"downloading {JSON_FILE}")
        self.d = self.connect_endpoint(self.thread_url)
        self.save_json(self.d)
        self.image_list = []

    def save_json(self, d):
        with open(JSON_FILE, "w") as f:
            json.dump(d, f, indent=2)

    def connect_endpoint(self, url):
        endpoint = f"{url}.json"  # see https://github.com/4chan/4chan-API
        r = requests.get(endpoint)
        return r.json()

    # based on https://github.com/jabbalaci/JSON-path
    def traverse(self, obj, images):
        if isinstance(obj, list):
            for subnode in obj:
                self.traverse(subnode, images)
        elif isinstance(obj, dict):
            if ("filename" in obj) and ("ext" in obj) and ("tim" in obj):
                ext = obj['ext']
                if ext in (".png", ".jpg"):
                    fname = f"{obj['tim']}{ext}"
                    url = f"{CDN_BASE_URL}/{self.board_id}/{fname}"
                    images.append(url)
                    # print(url)
            for v in obj.values():
                self.traverse(v, images)

    def find_images(self):
        images = []
        self.traverse(self.d, images)
        return images


def print_help():
    print("""
Usage: {0} <4chan_thread_url>
""".strip().format(sys.argv[0]))


def main():
    thread_url = sys.argv[1]
    down = Downloader(thread_url)
    li = down.find_images()
    log.info(f"number of images: {len(li)}")
    with open("down.txt", "w") as f:
        for url in li:
            print(url, file=f)
        #
    #
    log.info("image list was written to down.txt")

##############################################################################

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
        exit(1)
    # else
    main()
