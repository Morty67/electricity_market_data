from django.test import TestCase
from energy_market.models import MarketClosingData
from django.core.exceptions import ValidationError


class MarketClosingDataTestCase(TestCase):
    def test_model_string_representation(self):
        data = MarketClosingData(
            date="2023-06-11", hour="08", price=10.50, volume=100.5
        )
        expected_string = "MarketClosingData: 2023-06-11 08"
        self.assertEqual(str(data), expected_string)

    def test_model_fields(self):
        data = MarketClosingData(
            date="2023-06-11", hour="08", price=10.50, volume=100.5
        )
        self.assertEqual(data.date, "2023-06-11")
        self.assertEqual(data.hour, "08")
        self.assertEqual(data.price, 10.50)
        self.assertEqual(data.volume, 100.5)


def test_model_field_validators(self):
    # Test that invalid date format raises a validation error
    with self.assertRaises(ValidationError):
        data = MarketClosingData(
            date="2023/06/11", hour="08", price=10.50, volume=100.5
        )
        data.full_clean()

    # Test that negative price raises a validation error
    with self.assertRaises(ValidationError):
        data = MarketClosingData(
            date="2023-06-11", hour="08", price=-10.50, volume=100.5
        )
        data.full_clean()

    # Test that negative volume raises a validation error
    with self.assertRaises(ValidationError):
        data = MarketClosingData(
            date="2023-06-11", hour="08", price=10.50, volume=-100.5
        )
        data.full_clean()
