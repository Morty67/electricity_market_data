import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import schedule
import time

import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "electricity_market_data.settings"
)
django.setup()

from energy_market.models import MarketClosingData


def get_html_content(url):
    response = requests.get(url)
    return response.content


def parse_electricity_data(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("tbody")
    rows = table.find_all("tr")
    result = []

    for row in rows:
        fields = row.find_all("td")
        hour = re.search(r"\d+", fields[0].text.strip()).group()
        price = re.search(r"\d+\.\d+", fields[1].text.strip()).group()
        volume = re.search(r"\d+\.\d+", fields[3].text.strip()).group()
        result.append((hour, price, volume))

    return result


def save_data_to_database(data, date):
    if not MarketClosingData.objects.filter(date=date).exists():
        for hour, price, volume in data:
            MarketClosingData.objects.create(
                date=date, hour=hour, price=float(price), volume=float(volume)
            )
        print("The data has been successfully saved in the database.")
    else:
        print("The data for the given date already exists in the database.")


def run_parser():
    DATE = (datetime.now().date() + timedelta(days=1)).strftime("%d.%m.%Y")
    URL = f"https://www.oree.com.ua/index.php/PXS/get_pxs_hdata/{DATE}/DAM/2"

    html_content = get_html_content(URL)
    data = parse_electricity_data(html_content)
    date = datetime.strptime(DATE, "%d.%m.%Y").date()
    save_data_to_database(data, date)


if __name__ == "__main__":
    TIME = "12:35"
    schedule.every().day.at(TIME).do(run_parser)

    while True:
        schedule.run_pending()
        time.sleep(1)
