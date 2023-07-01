import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_currency():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                      "Safari/537.36"
    }
    url = "https://www.cbr.ru/currency_base/daily/"

    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    table = soup.find("table", class_="data").find_all("tr")

    for td in table:
        tds = [td.text.replace('\xa0', ' ') for td in td.find_all('td')]
        if "USD" in tds:
            result = tds

    date = f"{datetime.now().strftime('%d.%m.%Y')}"

    new_dict = {
        "date": date,
        "USD":  result[4]
    }

    with open("currency_base.json", "w") as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_currency()