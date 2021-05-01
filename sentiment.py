""" This script is for analysing sentiment of stocks traded through strategy.py"""

import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from finbert.finbert import predict
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def get_sentiment(stock_ticker):
    """
    This function extracts the last 100 headlines of a given stock from finviz.com and then analyses their sentiment using the finBERT sentiment analyser.

    Parameters
    ----------
    stock_ticker: Stock ticker string (ex: NRZ)

    Returns
    -------
    finbert_sentiment: The sentiment score of the headlines listed in finviz.com for a given stock ticker

    """

    stock_ticker = re.sub(r"\.", "-", stock_ticker)

    finviz_url = 'https://finviz.com/quote.ashx?t='

    news_tables = {}
    
    url = finviz_url + stock_ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[stock_ticker] = news_table
    
    
    parsed_data = []
    
    for stock_ticker, news_table in news_tables.items():
        for row in news_table.findAll('tr'):
            title = row.a.text
            date_data = row.td.text.split(' ')
    
            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]
    
            parsed_data.append([stock_ticker, date, time, title])
    
    df = pd.DataFrame(parsed_data, columns=['stock_ticker', 'date', 'time', 'title'])
    
    model = AutoModelForSequenceClassification.from_pretrained("pytorch_model")
    bert_sentiment = lambda x: predict(x, AutoModelForSequenceClassification.from_pretrained("pytorch_model"))['sentiment_score'].mean()
    
    headlines = '. '.join(df['title'].tolist())
    finbert_sentiment = bert_sentiment(headlines)
    return(finbert_sentiment)


#sentiment = get_sentiment(stock_ticker)
#print(sentiment)









