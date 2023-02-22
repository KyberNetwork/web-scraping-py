from typing import *
from logzero import logger as log
from bs4 import BeautifulSoup as Bs
import requests

url = 'https://coinmarketcap.com'

headers = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "accept-encoding": 'gzip, deflate, br',
    "accept-language": 'en-GB,en;q=0.9',
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": '?0',
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": 'document',
    "sec-fetch-mode": 'navigate',
    "sec-fetch-site": 'none',
    "sec-fetch-user": '?1',
    "upgrade-insecure-requests": '1',
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

def get_home() -> Bs:
    global url
    session = requests.Session()
    resp = session.get(url, headers=headers)
    html = Bs(resp.text, "html.parser")
    return html


def read_coins_symbol(html: Bs) -> List[str]:
    coins = []
    for e in html.select(".coin-item-symbol"):
        coins.append(e.getText())

    for e in html.select(".crypto-symbol"):
        coins.append(e.getText())

    return coins
