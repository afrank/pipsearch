#!/usr/bin/python3

import sys
import shutil

import requests
import json

from bs4 import BeautifulSoup

def search_pypi(q):

    url = "https://pypi.org/search/"

    page = requests.get(url, params={"q": q}).text

    soup = BeautifulSoup(page, 'html.parser')

    results = soup.find_all('a', class_="package-snippet")

    out = []

    for res in results:
        r = {}
        r["name"] = res.find('span', class_='package-snippet__name').get_text()
        r["latest"] = res.find('span', class_='package-snippet__version').get_text()
        #ts = res.find('time')["datetime"]
        r["summary"] = res.find('p', class_='package-snippet__description').get_text()
        r["score"] = 1
        out += [r]

    return out

def main():
    q = " ".join(sys.argv[1:]).strip()
    if not q:
        print("Must provide something to search for!")
        sys.exit(2)
    
    max_width = shutil.get_terminal_size((80, 20))[0]

    result = search_pypi(q)

    try:
        max_n = max([ len(x["name"]) for x in result ]) + 2
    except:
        max_n = 20

    max_v = 16

    max_s = max_width - max_v - max_n - 3
    if max_s > 100:
        max_s = 100

    line = "NAME".ljust(max_n) + "DESCRIPTION".ljust(max_s) + "LATEST".rjust(max_v)
    print(line)

    for r in result:
        score = r["score"]
        latest = r["latest"]
        summary = r["summary"]
        name = r["name"]

        line = ""
        line += name.ljust(max_n)
        if len(summary) > max_s:
            summary = summary[0:max_s-3] + "..."

        line += summary.ljust(max_s)

        if len(latest) > max_v:
            latest = latest[0:max_v]

        line += latest.rjust(max_v)

        print(line)

if __name__ == '__main__':
    main()
