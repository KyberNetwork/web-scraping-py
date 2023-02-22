from typing import *
from logzero import logger as log
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# chrome = ChromeDriverManager().install()
# driver = webdriver.Chrome(service=Service(chrome), options=options)
# driver.get("https://www.coinmarketcap.com/")
# log.info(driver.title)
# driver.quit()

import requests
from bs4 import BeautifulSoup as Bs
import coinmarketcap as cmk


html = cmk.get_home()
coins = cmk.read_coins_symbol(html)
log.info(coins)
