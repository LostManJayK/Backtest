import requests
from typing import * #Allows us to specify the type of query_parameters
import logging

logger = logging.getLogger()

class BinanceClient:

    def __init__(self, futures=False):

        self.futures = futures #Check if the user wishes to use futures trading
        self._exchange = "Binance"

        #Set the base URL for futures or spot trading
        if self.futures:
            self._base_url = "https://fapi.binance.com" #Underscore at start indicates private variable
        else:
            self._base_url = "https://api.binance.com"
            
        #self.symbols = self._get_symbols()

    #Create method for making requests
    def _make_request(self, endpoint: str, query_parameters: Dict):
        
        #Pull data from Binance based on query_parameters
        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)
            return None


        if response.status_code == 200: #200 indicates user success
            return response.json()
        else:
            logger.error("Error while making request to %s: %s (status code = %s)", endpoint, response.json(), response.status_code) #Review string formatting
            return None

    #Method to get symbols from binance
    def _get_symbols(self) -> List[str]:
        
        params = dict() #Parameters for request
        
        endpoint = "/fapi/v1/exchangeInfo" if self.futures else "/api/v3/exchangeInfo" #Sets endpoint based on futures or spot. Get endpoint from binance API info
        data = self._make_request(endpoint, params)
        
        symbols = [x["symbol"] for x in data["symbols"]]
        if self.futures:
            print("\n\nAvailable Binance Futures Token Pairs:\n")
            print(symbols)
        else:
            print("\n\nAvailable Binance Spot Token Pairs:\n")
            print(symbols)
        
        return symbols
    
    #Create method for getting historical candles
    def get_historical(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None): #Times will be int since we are using the unix epoch
        
        #Set the parameters for the historical data request. Check the Binance API for more info
        params = dict()
        
        params["symbol"] = symbol #Trading symbol
        params["interval"] = "1m" #Length of candlestick
        params["limit"] = 1500 #This denotes the number of candlessticks we wish to retreive
        
        if start_time is not None:
            params["start_time"] = start_time #Open time of candlestick
        if end_time is not None:
            params["end_time"] = end_time #Close time of candlestick
        
        #Retreive raw candle data from Binance
        endpoint = "/fapi/v1/klines" if self.futures else "/api/v3/klines"
        raw_candles = self._make_request(endpoint, params)
        
        #Create a list to store formatted candle data
        candles = []
        
        #Add candle info to created list
        if raw_candles is not None: #Verify that the request was successful
            for c in raw_candles:
                candles.append((float(c[0])/1000, float(c[1]), float(c[2]), float(c[3]), float(c[4]))) #Open time, Open price, High Price, Low Price, Close Price. Check Kline/Candlstick info in API
            return candles
        else:
            return None