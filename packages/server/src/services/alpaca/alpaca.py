# @Author: Omer Siddiqui
# File with helper function to retrieve stock info from Alpaca Markets API

import requests
#from config import APCA_API_KEY, APCA_API_SECRET

APCA_API_KEY = 'PK6OU4VE4ULW9H037IJR'
APCA_API_SECRET = 'B2shlnpi2YVCrAutPngoVZSbCInfG6citfu1HUuP'

# Alpaca API Endpoint
api_host = "https://data.alpaca.markets/v2/stocks/trades"
# Setup headers for JSON Request
headers = {
    "APCA-API-KEY-ID": APCA_API_KEY,
    "APCA-API-SECRET-KEY": APCA_API_SECRET,
    "accept": "application/json"
}
class AlpacaService:
    
    def get_latest_alpaca_quote(self, symbol:str):
        """ Sends a GET Request to Alpaca API to retrieve latest quote"""
        # Construct request url
        latest_url = f"{api_host}/latest?symbols={symbol}&feed=iex"
        print(latest_url)
        # Create response object
        response = requests.get(latest_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)

            # Get price from latest trades
            price = response_data["trades"][symbol]["p"]
            # Get timestamp
            timestamp = response_data["trades"][symbol]["t"]
            #print(timestamp)

            data = {
                "symbol": symbol,
                "price": price,
                "timestamp": timestamp
            }

            return data
            
        # Otherwise print error message
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_historical_alpaca_quote(self, symbol: str, start_time, end_time, quote_limit: int):
        """Sends GET request to Alpaca API to get the latest historical quotes"""
        
        # Convert start and end time string to appropriate format for request
        start_time = start_time.replace(':' , '%3A')
        print(start_time)
        end_time = end_time.replace(':' , '%3A')
        print(end_time)
        # Construct request url
        historical_url = f"{api_host}?symbols={symbol}&start={start_time}&end={end_time}&limit={quote_limit}&feed=iex&currency=USD"
        # Create response object
        response = requests.get(historical_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)

        # Otherwise print error message
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
# Sample Tests
"""
alpaca = AlpacaService()
alpaca.get_latest_alpaca_quote("AAPL")

alpaca.get_historical_alpaca_quote('AAPL', '2022-01-03T00:00:00Z', '2022-01-04T00:00:00Z', 10)
"""