# Description: Unit tests for StockPortfolioManager, covering data fetching, error handling, and UI updates.

import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from stock_portfolio_manager import StockPortfolioManager

# Initialize a Qt application (required for UI tests)
app = QApplication([])

class TestStockPortfolioManager(unittest.TestCase):
    def setUp(self):
        # Initialize the Stock Portfolio Manager window
        self.window = StockPortfolioManager()

    @patch("stock_portfolio_manager.requests.get")
    def test_fetch_stock_data_multiple_symbols(self, mock_get):
        # Mock API response data for multiple symbols
        mock_response_data = {
            "Time Series (1min)": {
                "2023-10-31 16:00:00": {
                    "1. open": "305.12",
                    "2. high": "306.30",
                    "3. low": "304.50",
                    "4. close": "305.00",
                    "5. volume": "1500"
                }
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        # Update symbols for test
        self.window.symbols = ["AAPL", "MSFT", "GOOGL"]

        # Call the fetch_stock_data method
        self.window.fetch_stock_data()

        # Check if table has correct rows for each symbol
        self.assertEqual(self.window.stock_table.rowCount(), 3)
        self.assertEqual(self.window.stock_table.item(1, 0).text(), "MSFT")
        self.assertEqual(self.window.stock_table.item(2, 0).text(), "GOOGL")

    @patch("stock_portfolio_manager.requests.get")
    def test_fetch_stock_data_api_failure(self, mock_get):
        # Simulate API failure
        mock_get.return_value.status_code = 500

        # Call fetch_stock_data and verify no rows added
        self.window.symbols = ["AAPL"]
        self.window.fetch_stock_data()
        self.assertEqual(self.window.stock_table.rowCount(), 0)

if __name__ == "__main__":
    unittest.main()

# Future Improvements:
# - Add more tests for edge cases.
# - Validate table updates for accurate change calculations.
