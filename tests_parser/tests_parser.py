import unittest
from unittest.mock import patch

from electricity_parser import parse_electricity_data, save_data_to_database


class MyParserTestCase(unittest.TestCase):
    @patch("electricity_parser.MarketClosingData.objects")
    def test_failed_connection(self, mock_objects):
        # Test the scenario when the connection to the webpage fails or returns incorrect content

        date = "01.01.2023"
        url = (
            f"https://www.oree.com.ua/index.php/PXS/get_pxs_hdata/{date}/DAM/2"
        )

        with patch("electricity_parser.get_html_content", return_value=None):
            # Verify that the parser handles a failed connection gracefully
            save_data_to_database([], date)

        with patch(
            "electricity_parser.get_html_content",
            return_value=b"Incorrect content",
        ):
            # Verify that the parser handles incorrect content gracefully
            save_data_to_database([], date)

    @patch("electricity_parser.MarketClosingData.objects")
    def test_parse_electricity_data(self, mock_objects):
        html = """
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>10.5</td>
                            <td>15.2</td>
                            <td>20.1</td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>15.3</td>
                            <td>12.7</td>
                            <td>18.7</td>
                        </tr>
                    </tbody>
                """

        expected_result = [
            ("1", "10.5", "20.1"),
            ("2", "15.3", "18.7"),
        ]

        result = parse_electricity_data(html)

        self.assertEqual(result, expected_result)

    @patch("electricity_parser.MarketClosingData.objects")
    def test_save_data_to_database(self, mock_objects):
        data = [("1", "10.5", "20.1"), ("2", "15.3", "18.7")]
        date = "01.01.2023"

        # Assume the object doesn't exist in the database
        mock_filter = mock_objects.filter.return_value
        mock_filter.exists.return_value = False

        save_data_to_database(data, date)

        # Verify that the objects are created with the correct values
        mock_create = mock_objects.create
        self.assertEqual(mock_create.call_count, 2)
        mock_create.assert_any_call(
            date=date, hour="1", price=10.5, volume=20.1
        )
        mock_create.assert_any_call(
            date=date, hour="2", price=15.3, volume=18.7
        )

        # Assume the object already exists in the database
        mock_filter.exists.return_value = True

        save_data_to_database(data, date)

        # Verify that no objects are created if the data already exists
        self.assertEqual(mock_create.call_count, 2)

    @patch("electricity_parser.MarketClosingData.objects")
    def test_save_data_to_database_invalid_data(self, mock_objects):
        data = [
            ("1", "10.5", "20.1"),
            ("2", "15.3", "18.7"),
            ("3", "invalid", "25.2"),  # Invalid price format
            ("4", "12.7", "invalid"),  # Invalid volume format
        ]
        date = "01.01.2023"

        # Assume the object doesn't exist in the database
        mock_filter = mock_objects.filter.return_value
        mock_filter.exists.return_value = False

        # Verify that ValueError is raised for invalid data
        with self.assertRaises(ValueError):
            save_data_to_database(data, date)

    @patch("electricity_parser.MarketClosingData.objects")
    def test_save_data_to_database_existing_data(self, mock_objects):
        # Test saving data when the data already exists in the database

        data = [
            ("1", "10.5", "20.1"),
            ("2", "15.3", "18.7"),
        ]
        date = "01.01.2023"

        # Assume the object already exists in the database
        mock_filter = mock_objects.filter.return_value
        mock_filter.exists.return_value = True

        save_data_to_database(data, date)

        # Verify that no objects are created if the data already exists
        mock_create = mock_objects.create
        self.assertEqual(mock_create.call_count, 0)

    @patch("electricity_parser.MarketClosingData.objects")
    def test_save_data_to_database_empty_data(self, mock_objects):
        # Test saving empty data

        data = []
        date = "01.01.2023"

        save_data_to_database(data, date)

        # Verify that no objects are created when the data is empty
        mock_create = mock_objects.create
        self.assertEqual(mock_create.call_count, 0)

    @patch("electricity_parser.MarketClosingData.objects")
    def test_save_data_to_database_invalid_data_format(self, mock_objects):
        # Test saving data with invalid format

        data = [
            ("1", "10.5", "20.1"),
            ("2", "invalid", "18.7"),  # Invalid price format
            ("3", "15.3", "invalid"),  # Invalid volume format
        ]
        date = "01.01.2023"

        # Assume the object doesn't exist in the database
        mock_filter = mock_objects.filter.return_value
        mock_filter.exists.return_value = False

        # Verify that ValueError is raised for invalid data format
        with self.assertRaises(ValueError):
            save_data_to_database(data, date)
