'''
MIT License

Copyright (c) 2021 Josh Schiavone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

__author__ = 'Josh Schiavone'
__version__ = '1.0'
__license__ = 'MIT'

import os, sys
import time
import requests
import argparse
import random
import json

from headers.agents import Headers
from banner.banner import Banner

class Colors:
    # Console colors
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    C = '\033[36m'  # cyan
    GR = '\033[37m'  # gray
    BOLD = '\033[1m'
    END = '\033[0m'

class Configuration:
    DARKDUMP_ERROR_CODE_STANDARD = -1
    DARKDUMP_SUCCESS_CODE_STANDARD = 0

    DARKDUMP_MIN_DATA_RETRIEVE_LENGTH = 1
    DARKDUMP_RUNNING = False
    DARKDUMP_OS_UNIX_LINUX = False
    DARKDUMP_OS_WIN32_64 = False
    DARKDUMP_OS_DARWIN = False

    DARKDUMP_REQUESTS_SUCCESS_CODE = 200

    __darkdump_api__ = "https://darksearch.io/api/search"

class Platform(object):
    def __init__(self, execpltf):
        self.execpltf = execpltf

    def get_operating_system_descriptor(self):
        cfg = Configuration()
        clr = Colors()

        if self.execpltf:
            if sys.platform == "linux" or sys.platform == "linux2":
                cfg.DARKDUMP_OS_UNIX_LINUX = True
                print(clr.BOLD + clr.W + "Operating System: " + clr.G + sys.platform + clr.END)
            if sys.platform == "win64" or sys.platform == "win32":
                cfg.DARKDUMP_OS_WIN32_64 = True
                print(clr.BOLD + clr.W + "Operating System: " + clr.G + sys.platform + clr.END)
            if sys.platform == "darwin":
                cfg.DARKDUMP_OS_DARWIN = True
                print(clr.BOLD + clr.W + "Operating System: " + clr.G + sys.platform + clr.END)
        else: pass

    def clean_screen(self):
        if self.execpltf:
            if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
                os.system('clear')
            else: os.system('cls')
        else: pass

class Darkdump(object):
    def __init__(self, api, query):
        self.api = api
        self.query = query

    def crawl_api(self):
        hdrs = Headers()
        clr = Colors()
        cfg = Configuration()

        try:
            darksearch_url_response = requests.get(self.api, params=self.query)
            json_data = darksearch_url_response.json()
            #json_dump = json.dumps(json_data, indent=2)
            darksearch_url_response.headers["User-Agent"] = random.choice(hdrs.useragent)
        except requests.RequestException as re:
            print(clr.BOLD + clr.R + str(re) + clr.END)

        try:
            if json_data["total"] >= cfg.DARKDUMP_MIN_DATA_RETRIEVE_LENGTH: # data >= 1
                for key in range(0, 18):             
                    site_title = json_data['data'][key]['title']
                    site_onion_link = json_data['data'][key]['link']
                    print(clr.BOLD + clr.G + f"[+] Site Title: {site_title}\n\t> Onion Link: {clr.R}{site_onion_link}\n" + clr.END)              
        except IndexError:
            print(clr.BOLD + clr.R + f"[-] No results found for query: {self.query}\n" + clr.END)

def darkdump_main():
    cfg = Configuration()
    clr = Colors()
    bn = Banner()

    Platform(True).clean_screen()
    Platform(True).get_operating_system_descriptor()
    bn.LoadDarkdumpBanner()
    time.sleep(1.5)

    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--version",
                        help="returns darkdump's version",
                        action="store_true")
    parser.add_argument("-q",
                        "--query",
                        help="the keyword or string you want to search on the deepweb",
                        type=str,
                        required=True)
    parser.add_argument("-p",
                        "--page",
                        help="the page number to filter through the results that the search engine returns (default=1).",
                        type=int)

    args = parser.parse_args()

    if args.version:
        print(clr.BOLD + clr.B + f"Darkdump Version: {__version__}\n" + clr.END)

    elif args.query:
        if args.page: 
            query = {
                    'query': args.query,
                    'page': args.page
                    }
            print(clr.BOLD + clr.B + f"Searching For: {args.query} on page: {args.page}...\n" + clr.END)
            Darkdump(cfg.__darkdump_api__, query).crawl_api()
            cfg.DARKDUMP_RUNNING = True
        else:
            query = {
                'query': args.query,
                'page': 1
                }           
            print(clr.BOLD + clr.B + f"Searching For: {args.query} on page: 1...\n" + clr.END)
            Darkdump(cfg.__darkdump_api__, query).crawl_api()
            cfg.DARKDUMP_RUNNING = True

if __name__ == "__main__":
    darkdump_main()


