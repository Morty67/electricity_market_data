from decimal import Decimal
from django.test import TestCase
from energy_market.models import MarketClosingData
from energy_market.serializers import MarketClosingDataSerializer


class MarketClosingDataSerializerTestCase(TestCase):
    def setUp(self):
        self.market_data = MarketClosingData.objects.create(
            date="2023-06-11",
            hour="08",
            price=Decimal("10.50"),
            volume=Decimal("100.5"),
        )
        self.serializer = MarketClosingDataSerializer(
            instance=self.market_data
        )

    def test_get_hour(self):
        serializer = MarketClosingDataSerializer()

        # We pass an object that has an attribute "hour" with the value "08".
        obj = type("MockObject", (), {"hour": "08"})
        expected_result = "08:00"

        self.assertEqual(serializer.get_hour(obj), expected_result)

    def test_serializer_representation(self):
        expected_representation = {
            "date": "2023-06-11",
            "hour": "08:00",
            "price (грн/МВт.год)": "10.50",
            "volume (МВт.год)": "100.5",
        }
        self.assertEqual(self.serializer.data, expected_representation)

    def test_serializer_field_values(self):
        self.assertEqual(self.serializer.data["date"], "2023-06-11")
        self.assertEqual(self.serializer.data["hour"], "08:00")
        self.assertEqual(self.serializer.data["price (грн/МВт.год)"], "10.50")
        self.assertEqual(self.serializer.data["volume (МВт.год)"], "100.5")
