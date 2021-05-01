"""
This contains trading strategies and functions that rely on the Alpaca trading platform

"""

import alpaca_trade_api as tradeapi
import support
import sentiment
import datetime
from pytz import timezone
import traceback


APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL = "", "", ""


def main():
    global APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL

    # Set global env variables
    set_vars()
    current_stock = ''

    while True:
        try:

            stocks_list = ["BRK.B", "AMD", "AAPL", "MSFT", "AMZN", "FB", "GOOGL", "TSLA"]

            st = timezone('EST')

            if support.is_trading_hours():
                for stock_tickers in stocks_list:
                    now = datetime.datetime.now(st)
                    current_stock = stock_tickers

                    print(f"\n\nIs trading hours! Time is: {now}, stock is: {current_stock}")

                    # Interact with rest api at alpaca
                    api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY, api_version='v2',
                                        base_url=APCA_API_BASE_URL)

                    # Trading strategy
                    trading_strategy(api, stock_ticker=stock_tickers)
                    support.wait_time()

                    if not support.is_trading_hours():
                    	break

            if not support.is_trading_hours():

                for stock_tickers in stocks_list:
                    now = datetime.datetime.now(st)
                    current_stock = stock_tickers

                    print(f"\n\nIt is not trading hours. Time is: {now}, stock is: {current_stock}")

                    # Interact with rest api at alpaca
                    api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY, api_version='v2',
                                        base_url=APCA_API_BASE_URL)

                    # Get portfolio info
                    get_portfolio_info(api, stock_ticker=stock_tickers)


            
                # Wait 15 minutes before checking again if not trading hours
                now = datetime.datetime.now(st)
                print(f"\n\nIt is not trading hours! Time is: {now}.")
                #support.wait_time(seconds=900)

        except Exception as e:
            # support.wait_time()

            # Save error in .txt file
            with open("log.txt", 'a') as f:  # Use file to refer to the file object

                f.write("\n \n")
                f.write(f"Stock ticker was {current_stock}")
                f.write("\n \n")
                f.write(f"Time is: {datetime.datetime.now()}")
                f.write(f"'exception_type: '{type(e).__name__}, \n"
                        f"'error_reason': {e.args}, \n"
                        f"\n")
                f.write(f"Traceback is: {traceback.format_exc()}")
                print(f"Breaking because of an error: {e}")


def get_portfolio_info(api, stock_ticker):
    """
    This function gets various information about stocks held in your portfolio. 

    Parameters
    ----------
    api: Alpaca api object
    stock_ticker: Stock ticker string (ex: NRZ)

    Returns
    -------
    None
    
    """
    # Checking moving averages
    ma_200 = support.get_ma(api, stock_ticker=stock_ticker, days="200")
    print(f"200-day moving average of {stock_ticker} is",ma_200)
    ma_50 = support.get_ma(api, stock_ticker=stock_ticker, days="50")
    print(f"50-day moving average of {stock_ticker} is",ma_50)

    # Checking last trading price
    price = support.get_price(api,stock_ticker=stock_ticker).price
    
    account = api.get_account()

    # Checking Sentiment
    stock_sentiment = sentiment.get_sentiment(stock_ticker=stock_ticker)
    if stock_sentiment <= -0.5:
        print(f"News sentiment of {stock_ticker} is negative ({stock_sentiment}).")
    elif stock_sentiment > -0.5 and stock_sentiment < 0.5:
        print(f"News sentiment of {stock_ticker} is neutral ({stock_sentiment}).")
    elif stock_sentiment >= 0.5:
        print(f"News sentiment of {stock_ticker} is positive ({stock_sentiment}).")        

    # Checking stock position
    currently_own_this_stock = support.currently_own_this_stock(api, stock_ticker=stock_ticker)
    if currently_own_this_stock == 0:
        print(f"{stock_ticker} stock is currently not held.")
    else:
        print(f"{stock_ticker} stock is currently held.")    


    # Checking pending orders
    pending_buy = support.check_for_pending(api, stock_ticker=stock_ticker, trade_type="buy", day_range=5, zone='UTC', result_limit=200)    
    pending_sell = support.check_for_pending(api, stock_ticker=stock_ticker, trade_type="sell", day_range=5, zone='UTC', result_limit=200)
    
    ###############################
    # New Strategy
    ###############################

def trading_strategy(api, stock_ticker):
    """
    This function initializes your defined trading strategy based on buying and selling logics. 

    Parameters
    ----------
    api: Alpaca api object
    stock_ticker: Stock ticker string (ex: NRZ)

    Returns
    -------
    None
    
    """
    
    # Get portfolio info

    get_portfolio_info(api, stock_ticker)

    # Strategy
    
    if currently_own_this_stock == 1:

        if ma_50 > ma_200:
            if stock_sentiment <= -0.5:
                print(f"Golden cross found for {stock_ticker} but news sentiments are negative. Let's hold position.")
            elif stock_sentiment > -0.5 and stock_sentiment < 0.5:
                print(f"Golden cross found for {stock_ticker} and news sentiments are neutral. Let's hold position.")
            elif stock_sentiment >= 0.5:
                print(f"Golden cross found for {stock_ticker} and news sentiments are positive. Let's increase position.")
                support.submit_trade(limit_price=price*1.005, api=api, stock_ticker=stock_ticker, quantity=1, side='buy', trade_type='limit', time_in_force='day')

        if ma_50 < ma_200:
            if stock_sentiment <= -0.5:
                print(f"Death cross has been found for {stock_ticker} and news sentiments are negative. Let's exit position.")
                support.submit_trade(limit_price=price*0.995, api=api, stock_ticker=stock_ticker, quantity=1, side='sell', trade_type='limit', time_in_force='day')
            elif stock_sentiment > -0.5 and stock_sentiment < 0.5:
                print(f"Death cross has been found for {stock_ticker} and news sentiments are neutral. Let's exit position.")
                support.submit_trade(limit_price=price*0.995, api=api, stock_ticker=stock_ticker, quantity=1, side='sell', trade_type='limit', time_in_force='day')
            elif stock_sentiment >= 0.5:
                print(f"Death cross found for {stock_ticker} and news sentiments are positive. Let's exit position.")
                support.submit_trade(limit_price=price*0.995, api=api, stock_ticker=stock_ticker, quantity=1, side='sell', trade_type='limit', time_in_force='day')


    if currently_own_this_stock == 0:

        if ma_50 > ma_200:
            if stock_sentiment <= -0.5:
                print(f"Golden cross found for {stock_ticker} but news sentiments are negative. Let's wait for a better time to buy.")
            elif stock_sentiment > -0.5 and stock_sentiment < 0.5:
                print(f"Golden cross found for {stock_ticker} and news sentiments are neutral. It's a good time to buy.")
                support.submit_trade(limit_price=price*1.005, api=api, stock_ticker=stock_ticker, quantity=1, side='buy', trade_type='limit', time_in_force='day')
            elif stock_sentiment >= 0.5:
                print(f"Golden cross found for {stock_ticker} and news sentiments are positive. It's a good time to buy.")
                support.submit_trade(limit_price=price*1.005, api=api, stock_ticker=stock_ticker, quantity=1, side='buy', trade_type='limit', time_in_force='day')

        if ma_50 < ma_200:
            if stock_sentiment <= -0.5:
                print(f"Death cross has been found for {stock_ticker} and news sentiments are negative. Let's wait for better time to buy.")
            elif stock_sentiment > -0.5 and stock_sentiment < 0.5:
                print(f"Death cross has been found for {stock_ticker} and news sentiments are neutral. Let's wait for better time to buy.")
            elif stock_sentiment >= 0.5:
                print(f"Death cross found for {stock_ticker} and news sentiments are negative. Let's wait for better time to buy.")


    

# Initializing
def set_vars(secrets_file="secrets-alpaca.trading"):
    """
    This function initializes the credentials by setting APCA_API_KEY_ID, APCA_API_SECRET_KEY, and APCA_API_BASE_URL
    global variables from a specified .env file in the same directory

    Parameters
    ----------
    secrets_file: Default set to secrets-alpaca.env, can be any secrets file containing the

    Returns
    -------
    None

    """

    global APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL

    with open(f"{secrets_file}", 'r') as file:
        contents = file.read()
        env_vars = contents.replace('export ', '').split("\n")
        APCA_API_KEY_ID = env_vars[0].split("=")[1]
        APCA_API_SECRET_KEY = env_vars[1].split("=")[1]
        APCA_API_BASE_URL = env_vars[2].split("=")[1]


if __name__ == '__main__':
    main()
