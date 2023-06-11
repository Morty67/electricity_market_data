# Electricity Market Data
Script for collecting hourly electricity market closing data and Django-based API.

## Installing / Getting started:
```shell
Python 3 must be installed
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/electricity_market_data/tree/develop
cd electricity_market_data
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py migrate
python electricity_parser.py
python manage.py runserver
```


## Features:

*  Real-time data collection after closing at 12:30
*  Storage of information in a relational database
*  API endpoint at http://localhost:8000/api/market-closing-data/<date:date>/
*  Date format: "DD.MM.YYYY" (ex.- 12.06.2023)