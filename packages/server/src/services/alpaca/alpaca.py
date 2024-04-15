# @Author: Omer Siddiqui
# File with helper function to retrieve stock info from Alpaca Markets API

import requests
from config import APCA_API_KEY, APCA_API_SECRET


# Alpaca API Endpoint
api_host = "https://data.alpaca.markets/v2/stocks/trades/quotes/latest?"
# Setup headers for JSON Request
headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": APCA_API_KEY,
    "APCA-API-SECRET-KEY": APCA_API_SECRET
}


def get_alpaca_quote(symbol):
    """ Sends a GET Request to Alpaca API to retrieve quote"""
    # Construct request url
    url = f"{api_host}symbols={symbol}&feed=iex&currency=USD"
    # Create response object
    response = requests.get(url, headers=headers)

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

# Sample test
#print(get_alpaca_quote("TSLA"))