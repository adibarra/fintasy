# @Author: adibarra (Alec Ibarra), omer8 (Omer Siddiqui)
# @description: Helper function to retrieve stock info from Alpaca Markets API


import math
from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

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
    timestamp: datetime


class Cache:
    MAX_SIZE = 100

    def __init__(self, MAX_SIZE: int = MAX_SIZE):
        self.cache = {}
        self.MAX_SIZE = MAX_SIZE
        self.key_queue = deque()

    def get(self, key):
        return self.cache.get(key)

    def has(self, key):
        return key in self.cache

    def set(self, key, value):
        if self.has(key):
            self.key_queue.remove(key)
        else:
            if len(self.cache) >= self.MAX_SIZE:
                oldest_key = self.key_queue.popleft()
                del self.cache[oldest_key]
            self.cache[key] = (datetime.now(), value)
        self.key_queue.append(key)

    def delete(self, key):
        if key in self.cache:
            self.key_queue.remove(key)
            del self.cache[key]

    def clear(self):
        self.cache.clear()
        self.key_queue.clear()


CACHE = Cache(100)


# Dictionary to convert interval to datetime increment
intervalIncrement = {
    "5m" : timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "30m": timedelta(minutes=30),
    "1h" : timedelta(hours=1),
    "1d" : timedelta(days=1) 
}



class AlpacaService:
    def get_quote(self, symbol: str) -> dict | None:
        """Sends a GET Request to Alpaca API to retrieve latest quote"""
        # Check if the symbol is in the cache
        if CACHE.has(symbol):
            time, quote = CACHE.get(symbol)
            time_diff = datetime.now() - time

            if time_diff < timedelta(minutes=15):
                return quote

        # Construct request url
        latest_url = f"{api_host}/latest?symbols={symbol}&feed=iex"
        response = requests.get(latest_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            
            # Return none if response object is empty
            if response_data["trades"] == {}:
                return None
                

            price_cents = math.floor(response_data["trades"][symbol]["p"] * 100)
            timestamp_str = response_data["trades"][symbol]["t"]
            timestamp = datetime.strptime(timestamp_str[:-4], "%Y-%m-%dT%H:%M:%S.%f")
            timestamp = timestamp.replace(tzinfo=timezone.utc)

            quote = Quote(symbol, price_cents, timestamp)

            # Add the quote to the cache
            CACHE.set(symbol, asdict(quote))
            return asdict(quote)

        return None

    def get_historical_quote(self, symbol: str, start_time : datetime,  end_time : datetime , interval : str = "5m", quote_limit: int = 10, offset : int = 0):
        """Sends GET request to Alpaca API to get the latest historical quotes"""

        # Convert start and end time string to appropriate format for request
        start = str(start_time).split()
        start = start[0] + 'T' + start[1] + 'Z'
        # print(start)
        end = str(end_time).split()
        end = end[0] + 'T' + end[1] + 'Z'
        # print(end)
        # Construct request url
        historical_url = f"{api_host}?symbols={symbol}&start={start}&end={end}&limit={quote_limit}&feed=iex&currency=USD"
        # print(historical_url)
        # Create response object
        response = requests.get(historical_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()

            # Queue to store quotes
            q = deque()
            # Data array for return call
            data = []
            
            # print(f"{response_data["trades"][symbol][offset:]}\n\n")
            # Add each quote to our queue
            for quote in response_data["trades"][symbol][offset:]:
                q.append(quote)
            
            
            # print(f"Num Quotes: {len(q)}\n")

            # Get first quote
            quote = q[0]
            quoteTime = datetime.strptime(quote["t"][:-4], "%Y-%m-%dT%H:%M:%S.%f")
            # Start the interval time at the first quote
            intStartTime = quoteTime
            # print(intStartTime)

            while q:
                # Update intStartTime and intEndTime
                intStartTime = quoteTime
                intEndTime = intStartTime + intervalIncrement[interval]
                # While queue is not empty and within interval
                # Split up quotes according to the time interval
                numQuotes = 0
                totalTime = 0.0
                totalPriceCents = 0.0
                print(f"Interval Range: {intStartTime} - {intEndTime}")
                while q and quoteTime < intEndTime:
                    print(f"Quote time: {quoteTime}")
                    totalPriceCents += quote['p'] * 100
                    totalTime += quoteTime.timestamp()
                    numQuotes += 1
                    # Move to next quote
                    quote = q.popleft()
                    quoteTime = datetime.strptime(quote["t"][:-4], "%Y-%m-%dT%H:%M:%S.%f")
                    
                    
                # print("\n")
                # Average out entries over the interval
                if numQuotes:
                    pricecents = totalPriceCents / numQuotes
                    timestamp = totalTime / numQuotes
                    # Convert back to datetime object
                    timestamp = datetime.fromtimestamp(timestamp=timestamp)
                    # Add quote object to data array
                    quote_obj = Quote(symbol, pricecents, timestamp)
                    data.append(asdict(quote_obj))
                # Update interval
                intStartTime = intEndTime

            # print(data)
            return data

        # Otherwise print error message
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

