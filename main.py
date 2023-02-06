import logging #Used to log messages and data
from tabulate import tabulate #Used for formatting print output into tables
from datetime import datetime #Used for converting epoch time to human readable time

from exchanges.binance import BinanceClient #Import the created BinanceClient class from the binance module in the exchanges pakcage
from exchanges.kucoin import KucoinClient #Import created Kucoin client class from the kucoin module in the exchanges package

#Create logging object which logs at the debug level. DEBUG is minimum logging level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#Create a format for the logging messages
formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s") #time of log, logging level, logging message

#Use the following to save info to a file

#Stream handler setup
stream_handler = logging.StreamHandler() #IO stream
stream_handler.setFormatter(formatter) #Assign formatter to stream handler
stream_handler.setLevel(logging.INFO) #Stream handler displays logging at INFO level

#File handler setup
file_handler = logging.FileHandler("info.log") #FIle handler writing to file named "info.log"
file_handler.setFormatter(formatter) #Assign formatter to file handler
file_handler .setLevel(logging.DEBUG) #File handler displays logging at DEBUG level

#Add a handler to the main logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

'''
logger.info("This is an info log") #Display a log message at info level. This will write to the specificed file (info.log)
logger.debug("This is a debug log") #Display log message at debug level. This will write to the specificed file (info.log). This wont display in terminal
'''

EXCHANGE_LIST = {'binance': BinanceClient, 'kucoin': KucoinClient}

#Create function for printing tabulates candlestick data
def display_candle_data(market_candles: list):
    
    #Convert open and close times to human readable time
    for i in range(0, len(market_candles)):
        market_candles[i] = list(market_candles[i])
        market_candles[i][0] = datetime.fromtimestamp(int(market_candles[i][0]))
        
    formatted_candle_info = tabulate(market_candles, headers=(["Open Time", "Open Price", "High Price", "Low Price", "Close Price"]))
    print(formatted_candle_info)
    

#We want to know what the program will do. So we need to ask the user. Only execute if the main fileis started directly
if __name__ == "__main__":
    
    mode = input("Choose the program mode (data / backtest / optimize): ").lower() #data: get data, backtest: simple backtest, optimize: optimization
    
    exchange: str = None #User's desired exchange
    futures = None #Users desired mode of trading (futures or spot)
    
    #Show a list of the supported exchanges
    print("Supported Exchanges:")
    print([ex for ex in EXCHANGE_LIST])
    
    #Ask the user for their preffered exchange to test on. Keep asking until an appripriate exchange is entered
    while exchange not in EXCHANGE_LIST:
        exchange = input("Enter your desired exchange: ").lower()
    
    #Determine if the user wishes to use futures or spot trading
    while futures not in ("spot", "futures"):
        futures = input("Type \"spot\" for Spot trading or \"futures\" for Futures trading: ").lower()
    
    futures = True if "futures"==futures else False
    
    #Instantiate exchange client
    client = EXCHANGE_LIST[exchange](futures)  
    
    #Call the get_historical() method from the Client class to retreive candlestick data from Binance
    candles = client.get_historical('ETH-USDT')
    
    print(candles)
    
    display_candle_data(candles)

    
    
