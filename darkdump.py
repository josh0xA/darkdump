'''
MIT License
Copyright (c) 2024 Josh Schiavone

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

__version__ = 3

import sys
sys.dont_write_bytecode = True

import requests
from bs4 import BeautifulSoup
import os
import time

import argparse
import random
import re
import json

import socket

from headers.agents import Headers
from banner.banner import Banner

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from textblob import TextBlob


notice = '''
Note: 
    This tool is not to be used for illegal purposes.
    The author is not responsible for any misuse of Darkdump.
    May God bless you all.
    https://joshschiavone.com - https://github.com/josh0xA
'''

class Colors:
    W = '\033[0m'  # white 
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
    DARKDUMP_PROXY = False
    DARKDUMP_TOR_RUNNING = False 

    descriptions = []
    urls = []

    # Default Tor Browser SOCKS port is 9150 (9050 is used by the system daemon)
    __socks5init__ = "socks5h://localhost:9150"
    __darkdump_api__ = "https://ahmia.fi/search/?q="

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
        cfg = Configuration()
        if self.execpltf:
            if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
                os.system('clear')
            else: os.system('cls')
        else: pass

    def check_tor_connection(self, proxy_config, *, debug: bool = False):
        test_url = 'http://api.ipify.org' 
        try:
            response = requests.get(test_url, proxies=proxy_config, timeout=10)
            print(f"{Colors.BOLD + Colors.G}Tor service is active. {Colors.END}")
            print(f"{Colors.BOLD + Colors.P}Current IP Address via Tor: {Colors.END}{response.text}")
            return True  # Connection was successful
        except Exception as exc:
            print(f"{Colors.BOLD + Colors.R}Tor is inactive or not configured properly. Cannot scrape.{Colors.END}")
            if debug:
                # Provide the underlying reason when debug flag is set
                print(f"{Colors.BOLD + Colors.R}[DEBUG] Tor connectivity error: {exc}{Colors.END}")
            return False

class Darkdump(object):
    def clean_text(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        text = re.sub(r'[\r\n]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.strip()

    def extract_keywords(self, text):
        clean_text = self.clean_text(text)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(clean_text.lower())
        filtered_text = [word for word in word_tokens if word.isalnum() and not word in stop_words]
        freq_dist = FreqDist(filtered_text)
        keywords = list(freq_dist)[:18]
        return keywords

    def analyze_text(self, text):
        # Tokenize text
        words = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words and word.isalnum()]
        
        freq_dist = FreqDist(filtered_words)
        top_words = freq_dist.most_common(10)

        blob = TextBlob(text)
        sentiment = blob.sentiment

        return {
            'top_words': top_words,
            'sentiment': {
                'polarity': sentiment.polarity,  # -1 to 1 where 1 means positive statement
                'subjectivity': sentiment.subjectivity  # 0 to 1 where 1 is very subjective
            }
        }

    def sanitize_filename(self, url):
        keepcharacters = (' ', '.', '_', '-')
        return "".join(c for c in url if c.isalnum() or c in keepcharacters).rstrip()

    def generate_html(self, image_urls, base_url):
        filename = self.sanitize_filename(base_url) + '.html'
        filepath = os.path.join('dd_scrape_image_dump', filename)
        os.makedirs('dd_scrape_image_dump', exist_ok=True)
        html_content = '<html><head><title>Image Gallery</title></head><body>'
        for url in image_urls:
            html_content += f'<img src="{url}" alt="Image" style="padding: 10px; height: 200px;"><br>'
        html_content += '</body></html>'
        
        with open(filepath, 'w') as file:
            file.write(html_content)
        return filepath

    def extract_links(self, soup):
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def extract_metadata(self, soup):
        """Extract metadata from the page."""
        meta_data = {}
        for meta in soup.find_all('meta'):
            meta_name = meta.get('name') or meta.get('property')
            if meta_name:
                meta_data[meta_name] = meta.get('content')
        return meta_data

    def extract_emails(self, soup):
        text = soup.get_text()
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = email_pattern.findall(text)
        return emails

    def extract_document_links(self, soup):
        doc_types = [
            '.pdf', '.doc', '.docx', '.xlsx', '.xls', '.ppt', '.pptx',
            '.txt', '.csv', '.rtf', '.odt', '.ods', '.odp', '.epub',
            '.mobi', '.log', '.msg', '.wpd', '.wps', '.tex', '.vsd',
            '.xml', '.json', '.xps', '.md', '.code', '.mp3', '.wav',
            '.mp4', '.avi', '.mov', '.flv', '.wma', '.aac', '.dll',
            '.exe', '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2',
            '.vmdk', '.iso', '.bin', '.img', '.dmg'
        ]
        links = [a['href'] for a in soup.find_all('a', href=True) if any(doc_type for doc_type in doc_types if a['href'].endswith(doc_type))]
        return links


    def crawl(
        self,
        query,
        amount,
        use_proxy: bool = False,
        scrape_sites: bool = False,
        scrape_images: bool = False,
        debug_mode: bool = False,
        browser_type: str | None = None,
    ):
        """
        Crawl Ahmia results and optionally scrape target onion sites.

        Parameters
        ----------
        browser_type : str | None
            If provided, restrict the randomly-selected User-Agent header to the
            specified browser family (chrome, firefox, ie, edge, opera, safari,
            mobile).  Falls back to a completely random User-Agent when omitted.
        """
        # Determine an appropriate user-agent string
        if browser_type:
            try:
                user_agent = Headers.get_random_by_browser(browser_type)
            except ValueError:
                # Fallback to a fully random UA if an invalid browser_type slips
                # through (should be prevented by argparse choices).
                user_agent = random.choice(Headers.user_agents)
        else:
            user_agent = random.choice(Headers.user_agents)

        # ------------------------------------------------------------------ #
        # Debug helper – show chosen User-Agent when debug mode is enabled
        # ------------------------------------------------------------------ #
        if debug_mode:
            browser_lbl = browser_type if browser_type else "random"
            print(f"{Colors.BOLD}{Colors.C}[DEBUG] Using User-Agent ({browser_lbl}): "
                  f"{Colors.END}{user_agent}")

        headers = {"User-Agent": user_agent}
        proxy_config = (
            {'http': Configuration.__socks5init__, 'https': Configuration.__socks5init__}
            if use_proxy else {}
        )

        # Fetching the initial search page
        try:
            page = requests.get(Configuration.__darkdump_api__ + query, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='ahmiaResultsPage')  # Adjust based on actual result container ID
            second_results = results.find_all('li', class_='result')  # Adjust based on actual results tag and class
        except Exception as e:
            print(f"{Colors.BOLD + Colors.R} Error in fetching Ahmia.fi: {e} {Colors.END}")
            return

        seen_urls = set()  # This set will store URLs to avoid duplicates

        if scrape_sites:
            # Forward the debug flag so we reveal connection errors when requested
            if not Platform(True).check_tor_connection(proxy_config, debug=debug_mode):
                return

        for idx, result in enumerate(second_results[:min(amount, len(second_results))]):
            site_url = result.find('cite').text
            if "http://" not in site_url and "https://" not in site_url:
                site_url = "http://" + site_url

            if site_url in seen_urls:
                continue
            seen_urls.add(site_url)
            
            title = result.find('a').text if result.find('a') else "No title available"
            description = result.find('p').text if result.find('p') else "No description available"
            try:
                if scrape_sites:
                    try:
                        site_response = requests.get(site_url, headers=headers, proxies=proxy_config)
                        site_soup = BeautifulSoup(site_response.content, 'html.parser')
                        text_analysis = self.analyze_text(site_soup.get_text())
                        metadata = self.extract_metadata(site_soup)
                        links = self.extract_links(site_soup)
                        emails = self.extract_emails(site_soup)
                        documents = self.extract_document_links(site_soup)

                        if scrape_images:
                            images = site_soup.find_all('img')
                            image_urls = [img['src'] for img in images if img.get('src')]
                            image_urls = [url if url.startswith('http') else site_url + url for url in image_urls]

                            html_path = self.generate_html(image_urls, site_url)
                            images_str = f"{Colors.BOLD}| Images Gallery: {Colors.END}{Colors.G}{os.path.abspath(html_path)}{Colors.END}\n"

                        print('-' * 50)
                        print(f"{Colors.BOLD}{idx + 1}.\n --- [+] Website: {Colors.END}{Colors.P}{title.strip()}{Colors.END}")
                        print(f"{Colors.BOLD}| Information: {Colors.END}{Colors.G}{description.strip()}{Colors.END}")
                        print(f"{Colors.BOLD}| Onion Link: {Colors.END}{Colors.G}{site_url}{Colors.END}")
                        print(f"{Colors.BOLD}| Keywords: {Colors.END}{Colors.G}{', '.join(self.extract_keywords(site_soup.get_text()))}{Colors.END}")
                        print(f"{Colors.BOLD}\t- Sentiment: Polarity = {text_analysis['sentiment']['polarity']:.2f}, Subjectivity = {text_analysis['sentiment']['subjectivity']:.2f}")
                        print(f"{Colors.BOLD}| Metadata: {Colors.END}{Colors.G}{json.dumps(metadata)}{Colors.END}")
                        print(f"{Colors.BOLD}| Links Found: {Colors.END}{Colors.G}{len(links)}{Colors.END}")
                        print(f"{Colors.BOLD}| Emails Found: {Colors.END}{Colors.G}{', '.join(emails) if emails else 'No emails found.'}{Colors.END}")
                        print(f"{Colors.BOLD}| Documents Found: {Colors.END}{Colors.G}{', '.join(documents) if documents else 'No document links found.'}{Colors.END}")

                        if scrape_images:
                            if image_urls:
                                print(images_str)
                            else: print(f"{Colors.BOLD + Colors.GR} No images found. Skipping parse. {Colors.END}")

                    except Exception as e: 
                        print(f"{Colors.BOLD + Colors.O} Dead onion, skipping...: {site_url} {Colors.END}")
                        if debug_mode:
                            print(f"{Colors.BOLD + Colors.R}[DEBUG] Exception: {e}{Colors.END}")
	
                else: # No scrape
                    print(f"{Colors.BOLD}{idx + 1}. --- [+] Website: {Colors.END}{Colors.P}{title.strip()}{Colors.END}")
                    print(f"{Colors.BOLD}\t Information: {Colors.END}{Colors.G}{description.strip()}{Colors.END}")
                    print(f"{Colors.BOLD}| Onion Link: {Colors.END}{Colors.G}{site_url}{Colors.END}\n")


            except KeyboardInterrupt as ki:
                print(f"{Colors.BOLD + Colors.R} Quitting... {Colors.END}")


def darkdump_main():
    clr = Colors()
    bn = Banner()

    Platform(True).clean_screen()
    Platform(True).get_operating_system_descriptor()
    bn.LoadDarkdumpBanner()
    print(notice)

    parser = argparse.ArgumentParser(description="Darkdump is an interface for scraping the deepweb through Ahmia. Made by yours truly.")
    parser.add_argument("-v", "--version", help="returns darkdump's version", action="store_true")
    parser.add_argument("-q", "--query", help="the keyword or string you want to search on the deepweb", type=str)
    parser.add_argument("-a", "--amount", help="the amount of results you want to retrieve", type=int, default=10)
    parser.add_argument("-p", "--proxy", help="use tor proxy for scraping", action="store_true")
    parser.add_argument("-i", "--images", help="scrape images and visual content from the site", action="store_true")
    parser.add_argument("-s", "--scrape", help="scrape the actual site for content and look for keywords", action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug output", action="store_true")
    parser.add_argument(
        "-b", "--browser",
        help=("specify browser type for the User-Agent header "
              "(chrome, firefox, ie, edge, opera, safari, mobile)"),
        choices=['chrome', 'firefox', 'ie', 'edge', 'opera', 'safari', 'mobile'],
        type=str
    )

    args = parser.parse_args()

    if args.version:
        print(Colors.BOLD + Colors.B + f"Darkdump Version: {__version__}\n" + Colors.END)

    if args.proxy and not args.scrape:
        print(Colors.BOLD + Colors.R + "Error: Proxy option '-p' must be used with the scraping option '-s'." + Colors.END)
        parser.print_help()
        sys.exit(1)

    if args.images and not args.scrape:
        print(Colors.BOLD + Colors.R + "Error: Images option '-i' must be used with the scraping option '-s'." + Colors.END)
        parser.print_help()
        sys.exit(1)

    if args.debug:
        print(f"{Colors.R}DEBUG mode is on.{Colors.W}")

    if args.query:
        print(f"Searching For: {args.query} and showing {args.amount} results...\nIndexing is viable, skipping dead onions.\n")
        Darkdump().crawl(
            args.query,
            args.amount,
            use_proxy=args.proxy,
            scrape_sites=args.scrape,
            scrape_images=args.images,
            debug_mode=args.debug,
            browser_type=args.browser
        )
    else:
        print("[~] Note: No query arguments were passed. Please supply a query to search.")

if __name__ == "__main__":
    darkdump_main()
