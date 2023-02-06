import requests
from typing import *
import logging

#Instantiate logger object
logger = logging.getLogger()

#Create a class for the Kucoin client
class KucoinClient:
    
    def __init__(self, futures=False):
        
        self.futures = futures
        self._exchange = "Kucoin"
        
        #Set the base url for the Kucoin API
        self._base_url = "https://api-futures.kucoin.com" if self.futures else "https://api.kucoin.com"
        
        self.symbols = self._get_symbols()
        
    #create a method for making requests
    def _make_request(self, endpoint: str, query_parameters: Dict):
        
        #Attempt to make the query to Kucoin. Let the user know if the connection is unsuccessful
        try:
            response = requests.get(self._base_url+endpoint, params=query_parameters)
        except Exception as e:
            print("Error while making request to %s, %s", endpoint, e)
            return None
        
        #If the request was successful, return the response. If not display an error message
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making request to %s: %s (status code = %s)", endpoint, response.json(), response.status_code)
            return None
        
    #Create a method for retreiving symbols
    def _get_symbols(self) -> List[str]:
        
        params = dict() #For query parameters
        
        #Define endpoint based on market type (futures or spot)
        endpoint = "/api/v1/contracts/active" if self.futures else "/api/v2/symbols"
        
        #Request the data from the endpoint and store (expecting Dict())
        data = self._make_request(endpoint, params)
        
        #Get the list of symbols (Check Kucoin API)
        symbols = [x["symbol"] for x in data["data"]]
        
        if self.futures:
            print("\n\nAvailable Kucoin Futures Token Pairs:\n")
            print(symbols)
        else:
            print("\n\nAvailable Kucoin Spot Token Pairs:\n")
            print(symbols)
        
        return symbols
    
    #Create the method for retreiving historical data of a single symbol from Kucoin Futures
    def _get_historical_futures(self, symbol: str, granularity: int=1, start_time: Optional[int]=None, end_time: int=None):
        
        #Create object for request parameters (dict)
        params = dict()
        endpoint = "/api/v1/kline/query"
        
        #Specify parameters
        
        #Kucoin Futures
        params['symbol'] = symbol
        params['granularity'] = granularity #Length of the candle in minutes. Check Kucoin for available options
        
        #If we received start and end time, assign them. Note that maximum size of requst is 200
        if start_time is not None:
            params['from'] = start_time
        if end_time is not None:
            params['to'] = end_time
            
        #Get the candlestick data from Kucoin
        raw_candles = self._make_request(endpoint, params)
        
        #Create list to store formatted candlestick data
        candles=[]
        
        #Format the candlesstick data into a list
        if raw_candles is not None:
            for c in raw_candles['data']:
                candles.append((float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]))) #Open time, Open price, High Price, Low Price, Close Price. Check Kucoin Futures api for more info
            return candles
        else:
            return None
    
    #Method for retrieving historical data from the Kucoin Sport market
    def _get_historical_spot(self, symbol: str, type: str='1min', startAt: Optional[int]=None, endAt: Optional[int]=None):
        
        params = dict()
        endpoint = "/api/v1/market/candles"
        
        params['symbol']: str = symbol
        params['type']: str = type
        
        if startAt != None:
            params['startAt'] = startAt
        if endAt != None:
            params['endAt'] = endAt
            
        raw_candles = self._make_request(endpoint, params)
        print(raw_candles) #####
        candles = []
        
        if raw_candles is not None:
            for c in raw_candles['data']:
                candles.append((float(c[0]), float(c[1]), float(c[3]), float(c[4]), float(c[2]))) #Open time, Open price, High Price, Low Price, Close Price, Close time. Check Kucoin Futures api for more info
            return candles
        else:
            return None
        
    def get_historical(self, symbol: str, type=None, startAt: Optional[int]=None, endAt: Optional[int]=None):
        
        type = 1 if self.futures else '1min'
        
        if self.futures:
            return self._get_historical_futures(symbol, type, startAt, endAt)
        else:
            return self._get_historical_spot(symbol, type, startAt, endAt)
        
        
    
