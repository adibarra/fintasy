# @Author: adibarra (Alec Ibarra), omer8 (Omer Siddiqui)
# @description: Helper function to retrieve stock info from Alpaca Markets API

import datetime
from dataclasses import asdict, dataclass

import requests
from config import APCA_API_KEY, APCA_API_SECRET

api_host = "https://data.alpaca.markets/v2/stocks/trades"
headers = {
    "APCA-API-KEY-ID": APCA_API_KEY,
    "APCA-API-SECRET-KEY": APCA_API_SECRET,
    "accept": "application/json",
}


@dataclass
class Quote:
    symbol: str
    price_cents: int
    timestamp: datetime.datetime


CACHE_MAX_SIZE = 100
CACHE: dict[str, Quote] = {}


class AlpacaService:
    def get_quote(symbol: str) -> Quote | None:
        """Sends a GET Request to Alpaca API to retrieve latest quote"""
        # Check if the symbol is in the cache
        if symbol in CACHE:
            quote = CACHE[symbol]
            # Get current time
            current_time = datetime.datetime.now()
            # Get timestamp from cache
            timestamp = quote.timestamp
            # Calculate time difference
            time_diff = current_time - timestamp
            # Check if time difference is less than 15 minutes
            if time_diff.total_seconds() < 900:
                return quote

        # Construct request url
        latest_url = f"{api_host}/latest?symbols={symbol}&feed=iex"
        response = requests.get(latest_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()

            price_cents = response_data["trades"][symbol]["p"] * 100
            timestamp_str = response_data["trades"][symbol]["t"]
            timestamp = datetime.datetime.strptime(
                timestamp_str[:-4], "%Y-%m-%dT%H:%M:%S.%f"
            )

            quote = Quote(symbol, price_cents, timestamp)

            # Add the quote to the cache
            if len(CACHE) >= CACHE_MAX_SIZE:
                CACHE.popitem()
            CACHE[symbol] = asdict(quote)
            return asdict(quote)

        return None

    def get_historical_quote(symbol: str, start_time, end_time, quote_limit: int):
        """Sends GET request to Alpaca API to get the latest historical quotes"""

        # Convert start and end time string to appropriate format for request
        start_time = start_time.replace(":", "%3A")
        print(start_time)
        end_time = end_time.replace(":", "%3A")
        print(end_time)
        # Construct request url
        historical_url = f"{api_host}?symbols={symbol}&start={start_time}&end={end_time}&limit={quote_limit}&feed=iex&currency=USD"
        # Create response object
        response = requests.get(historical_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            # print(response_data)

            data = []
            for quote in response_data["trades"][symbol]:
                quote_data = {
                    "symbol": symbol,
                    "price_cents": quote["p"],
                    "timestamp": quote["t"],
                }
                data.append(quote_data)

            return data

        # Otherwise print error message
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
