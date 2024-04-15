# @Author: Omer Siddiqui
# File with helper function to retrieve stock info from Alpaca Markets API

import requests
import os
from dotenv import load_dotenv


# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Load environment variables from the .env.apca file
dotenv_path = os.path.join(script_dir, '.env.apca')
load_dotenv(dotenv_path)

# Access environment variables
api_key = os.getenv("APCA_API_KEY")
api_secret = os.getenv("APCA_API_SECRET")
api_host = os.getenv("APCA_API_HOST")

# Setup headers for JSON Request
headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": api_secret
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

        # Get adjusted price(ap)
        price = response_data["quotes"][symbol]["ap"]
        # if ap is 0 use bid price(bp) <- Note: Need to confirm if this is what we want to do
        if (not price):
            price = response_data["quotes"][symbol]["bp"]
        #print(f"price: {price}") # Check for price
        
        # Get timestamp
        timestamp = response_data["quotes"][symbol]["t"]
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