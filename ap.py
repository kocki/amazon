import json
from datetime import datetime, timedelta
from decimal import Decimal
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55"
                  " Safari/537.36"
}
PRICES = {}
PRICE_DROP = '♥♥♥︎'
PRICE_RAISE = '☹☹☹︎'


def check_price(item_with_comment):
    try:
        item = item_with_comment.split("#")[0].strip()
        if item.startswith("https://"):
            url = item
        else:
            url = f"https://www.amazon.co.uk/dp/{item}/"

        response = requests.get(
            url,
            headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup.encode('utf-8')

        title = soup.find(id="productTitle").get_text().strip()
        price_str = soup.find(class_="apexPriceToPay").find(
            class_="a-offscreen").string.replace(",", "")
        # print(price_str)
        price_str = re.findall(r'\d+\.?\d*', price_str)[0]
        # print(price_str)
        price = Decimal(price_str)

        if price != PRICES.setdefault(item, {"price": price})["price"]:
            if price < PRICES[item]['price']:
                print(f"{PRICE_DROP:12} | PRICE DROP")
            else:
                print(f"{PRICE_RAISE:12} | PRICE RAISE")
            msg = f"{price:>12} | {title} (was: {PRICES[item]['price']})"
            PRICES[item]['price'] = price
        else:
            msg = f"{price:>12} | {title}"
        print(msg)

    except Exception as exc:
        print("### Something wrong happened... ###")
        print(repr(exc))
        print(url)


while True:
    with open("ap.json", "r") as f:
        data = json.load(f)

    for item in data["items"]:
        if item:
            check_price(item)
            sleep_time = randint(11, 59)

            now = datetime.now()
            print(
                f"{' ':12} | {now.strftime('%H:%M:%S')}: Next read in {sleep_time} sec. (at {(now + timedelta(seconds=sleep_time)).strftime('%H:%M:%S')})")
            sleep(sleep_time)
