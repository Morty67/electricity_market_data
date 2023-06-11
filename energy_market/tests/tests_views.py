from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from energy_market.models import MarketClosingData
from energy_market.serializers import MarketClosingDataSerializer


class MarketClosingDataViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            "market-closing-data",
            args=[datetime.strptime("11-06-2023", "%d-%m-%Y").date()],
        )

        # Створюємо декілька екземплярів MarketClosingData для тестування
        MarketClosingData.objects.create(
            date="2023-06-11", hour="08", price=10.50, volume=100.5
        )
        MarketClosingData.objects.create(
            date="2023-06-11", hour="09", price=12.75, volume=80.2
        )

    def test_get_existing_market_data(self):
        response = self.client.get(self.url)
        market_data = MarketClosingData.objects.filter(date="2023-06-11")
        serializer = MarketClosingDataSerializer(market_data, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_market_data(self):
        url = reverse(
            "market-closing-data",
            args=[datetime.strptime("2023-06-12", "%Y-%m-%d").date()],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"message": "No data available for this date."}
        )

    def test_get_market_data_with_invalid_date(self):
        url = reverse(
            "market-closing-data",
            args=[datetime.strptime("2023-06-12", "%Y-%m-%d").date()],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {"message": "No data available for this date."}
        )
