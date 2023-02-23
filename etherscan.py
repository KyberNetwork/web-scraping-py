from typing import *
from bs4 import BeautifulSoup as Bs
import requests


def get_page(path: str, write_file: bool = False, read_cache: bool = False) -> Tuple[Bs, str]:
    if read_cache:
        f = open("content.txt", "r")
        content = f.read()
        f.close()
        html = Bs(content, "html.parser")
        return html, content

    headers = {
        "Host": "etherscan.io",
        "accept": "*/*",
        "user-agent": "curl/7.86.0"
    }

    session = requests.Session()
    resp = session.get(path, headers=headers)

    if write_file:
        f = open("content.txt", "w")
        f.write(resp.text)
        f.close()

    html = Bs(resp.text, "html.parser")
    return html, resp.text


def token_holder_page(token_addr: str, page: int) -> str:
    """50 addresses per page"""
    return f"https://etherscan.io/token/generic-tokenholders2?m=l&a={token_addr}&p={page}"


def read_tokens(html: Bs) -> List[Tuple[str, str, str]]:
    """get list tokens"""
    tokens = []
    rows = html.select("tr")

    for row in rows[1:]:
        anchors = row.select("a")
        token_addr = anchors[0]["href"][7:]
        token_name = anchors[0].select("div:first-child")[0].getText()
        token_symbol = anchors[0].select("span")[0].getText()[1:-1]
        tokens.append((token_name, token_symbol, token_addr))

    return tokens


def read_holders(html: Bs) -> List[Tuple[str, str, float, float]]:
    holders = []

    for row in html.select("tr")[1:]:
        try:
            holder_name = row.select("a[target=_parent]")[0].getText()
            tooltip = row.select("a.link-secondary[data-bs-toggle=tooltip]")[0]
            holder_address = tooltip.get("data-clipboard-text") or tooltip.get("title")
            quantity = float(row.select("td")[2].getText().replace(",", ""))
            value_in_str = row.select("td")[4].getText()
            value_as_float = float(value_in_str[1:].replace(",", ""))
            holders.append((holder_name, holder_address, quantity, value_as_float))
        except Exception as e:
            # Possibly no holders info
            continue

    return holders


def read_top_tokens(top: int = 50) -> List[Tuple[str, str, str]]:
    tokens = []
    page = 1

    while len(tokens) < top:
        html, _ = get_page(f"https://etherscan.io/tokens?p={page}")
        tokens += read_tokens(html)
        page += 1

    return tokens


def read_top_holders(token_addr: str, top: int = 50) -> List[Tuple[str, str, float, float]]:
    """Get top token holders, return Alias, Address, Quantity, Value"""
    result = []
    page = 1

    while len(result) < top:
        url = token_holder_page(token_addr, page)
        html, _ = get_page(url)
        holders = read_holders(html)
        result += holders

        if len(holders) < 50:
            break

        page += 1

    return result
