import datetime as dt

from django.urls import register_converter


class DateConverter:
    regex = r"\d{2}\.\d{2}\.\d{4}"

    def to_python(self, value):
        day, month, year = value.split(".")
        return dt.date(int(year), int(month), int(day))

    def to_url(self, value):
        return value.strftime("%d.%m.%Y")


register_converter(DateConverter, "date")
