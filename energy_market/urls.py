from django.urls import path, register_converter

from energy_market.utils.date_converter import DateConverter
from energy_market.views import MarketClosingDataView


register_converter(DateConverter, "date")

urlpatterns = [
    path(
        "market-closing-data/<date:date>/",
        MarketClosingDataView.as_view(),
        name="market-closing-data",
    ),
]
