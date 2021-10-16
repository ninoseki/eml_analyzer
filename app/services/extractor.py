from typing import List

import html2text
from bs4 import BeautifulSoup
from ioc_finder import parse_urls
import re
import urllib.parse


def is_html(content_type: str) -> bool:
    return "text/html" in content_type


def desafelink_url(url: str):
    # convert a Microsoft safelink back to a normal URL
    match = re.search(r"https?://[^/]+\.safelinks\.protection\.outlook\.com/\?url=([^&]+)", url)
    if match:
        url = urllib.parse.unquote(match.group(1))

    return url


def desafelink_urls(urls: List[str]) -> List[str]:
    return [desafelink_url(url) for url in urls]


def normalize_url(url: str):
    # remove ] and > from the end of the URL
    url = url.rstrip(">")
    url = url.rstrip("]")
    return url


def normalize_urls(urls: List[str]) -> List[str]:
    unique_urls = list(set(urls))
    return [normalize_url(url) for url in unique_urls]


def get_href_links(html: str) -> List[str]:
    soup = BeautifulSoup(html)
    links: List[str] = [str(link.get("href")) for link in soup.findAll("a")]
    return [
        link
        for link in links
        if link.startswith("http://") or link.startswith("https://")
    ]


def parse_urls_from_body(content: str, content_type: str) -> List[str]:
    urls: List[str] = []

    if is_html(content_type):
        # extract href links
        urls.extend(get_href_links(content))

        # convert HTML to text
        h = html2text.HTML2Text()
        h.ignore_links = True
        content = h.handle(
            "<p>Hello, <a href='https://www.google.com/earth/'>world</a>!"
        )

    urls.extend(parse_urls(content, parse_urls_without_scheme=False))
    return desafelink_urls(normalize_urls(urls))
