#!/usr/bin/python3

import sys
import shutil

import requests
import json

from bs4 import BeautifulSoup

def search_pypi(q, url="https://pypi.org/search/"):
    """
    Perform a search on pypi.org and parse the results.

    we are looking for name, summary and latest version.
    """

    page = requests.get(url, params={"q": q}).text

    soup = BeautifulSoup(page, 'html.parser')

    results = soup.find_all('a', class_="package-snippet")

    out = []

    for res in results:
        r = {}
        r["name"] = res.find('span', class_='package-snippet__name').get_text()
        r["latest"] = res.find('span', class_='package-snippet__version').get_text()
        #ts = res.find('time')["datetime"] # we could return date of most recent change
        r["summary"] = res.find('p', class_='package-snippet__description').get_text()
        out += [r]

    return out

def main():
    """
    #
    # the output has 3 columns: name, summary and latest version.
    #
    # we cannot truncate the name, because that's what the user needs most.
    # so we find the max length of the names in the result and use that as the name
    # width. This is max_n.
    #
    # we set the max length of the version string to 16 characters. max_v.
    #
    # then we subtract the version and name lengths from the total width and that is
    # what is left over for the summary string. However, some users (like me) have very
    # wide consoles, and letting it use it all will put the version string in no-mans-land,
    # so we set a maximum summary string length of 100 characters.
    """

    q = " ".join(sys.argv[1:]).strip()
    if not q:
        print("Must provide something to search for!")
        sys.exit(2)
    
    # get the total max width of the console, with a default of 80
    max_width = shutil.get_terminal_size((80, 20))[0]

    # perform the search query
    result = search_pypi(q)

    # get the column width for the name
    try:
        max_n = max([ len(x["name"]) for x in result ]) + 2
    except:
        max_n = 20

    # column width for the version
    max_v = 16

    # column width for the summary
    max_s = min(100, max_width - max_v - max_n - 3)

    # print the top line
    print("NAME".ljust(max_n) + "DESCRIPTION".ljust(max_s) + "LATEST".rjust(max_v))

    for r in result:
        latest = r["latest"]
        summary = r["summary"]
        name = r["name"]

        line = ""

        line += name.ljust(max_n)

        if len(summary) > max_s:
            summary = summary[:max_s-3] + '...'
        line += summary.ljust(max_s)

        latest = latest[:max_v]
        line += latest.rjust(max_v)

        print(line)

if __name__ == '__main__':
    main()
