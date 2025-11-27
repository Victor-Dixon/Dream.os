# Description: PyQt5 Stock Portfolio Manager with Alpha Vantage data fetching, including error handling.
# Displays stock data in a table with periodic updates and error notifications.

import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class StockPortfolioManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Stock Portfolio Manager")
        self.setGeometry(100, 100, 600, 400)

        # Set up main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Initialize stock table
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(3)
        self.stock_table.setHorizontalHeaderLabels(["Symbol", "Price", "Change"])
        layout.addWidget(self.stock_table)

        # Symbols to fetch
        self.symbols = ["AAPL", "TSLA", "GOOGL"]

        # Timer for data updates (every minute)
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_stock_data)
        self.timer.start(60000)  # 1 minute

        # Fetch initial data
        self.fetch_stock_data()

    def fetch_stock_data(self):
        """Fetch stock data from Alpha Vantage and update the table."""
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            self.show_error("API Key Missing", "Please check your .env file for the API key.")
            return

        data = []
        for symbol in self.symbols:
            try:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}"
                response = requests.get(url)
                response.raise_for_status()
                json_data = response.json()

                # Check for valid data structure
                if "Time Series (1min)" not in json_data:
                    raise ValueError(f"No intraday data available for {symbol}")

                latest_data = list(json_data["Time Series (1min)"].values())[0]
                price = float(latest_data["1. open"])
                change = self.calculate_change(price, symbol)
                data.append({"symbol": symbol, "price": price, "change": change})
                
            except (requests.RequestException, ValueError) as e:
                print(f"Error fetching data for {symbol}: {e}")
                self.show_error("Data Fetch Error", f"Failed to fetch data for {symbol}.")
        
        # Update the table with fetched data if available
        if data:
            self.update_table(data)

    def calculate_change(self, price, symbol):
        # Placeholder for calculating percentage change
        return "+0.5%"

    def update_table(self, data):
        """Updates the stock table with provided data."""
        self.stock_table.setRowCount(len(data))
        for row, stock in enumerate(data):
            self.stock_table.setItem(row, 0, QTableWidgetItem(stock["symbol"]))
            self.stock_table.setItem(row, 1, QTableWidgetItem(f"${stock['price']:.2f}"))
            self.stock_table.setItem(row, 2, QTableWidgetItem(stock["change"]))

    def show_error(self, title, message):
        """Display error messages in a message box."""
        QMessageBox.critical(self, title, message)

# Example Usage
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockPortfolioManager()
    window.show()
    sys.exit(app.exec_())

# Future Improvements:
# - Add more robust change calculations.
# - Expand error handling to cover more scenarios.
# - Enhance UI with more stock details and trends.
