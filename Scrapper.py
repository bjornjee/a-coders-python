from yahoo_fin.stock_info import *
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os

class Scrapper:
    def __init__(self):
        #setup mongo
        DB_HOST = "localhost" if (os.getenv("DB_HOST") is None) else os.getenv("DB_HOST")
        DB_NAME = "acoders" if (os.getenv("DB_NAME") is None) else os.getenv("DB_NAME")
        client = MongoClient(DB_HOST,27017)
        db = client[DB_NAME]
        self.market_data = db.market_data

    def scrape(self,tickers_df):
        #count = self.market_data.count()
        tickers = tickers_df['Ticker'].to_numpy()
        instruments = tickers_df['Instrument'].to_numpy()
        count = 0
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(now)
        col = ['_id','datetime','ticker','instrument','Quote Price','Volume','Open','Previous Close','PE Ratio (TTM)']
        df = pd.DataFrame(columns=col)
        info = ['PE Ratio (TTM)','Open','Previous Close','Quote Price','Volume']
        for i  in range(len(tickers)):
            count += 1
            curr_ticker = tickers[i]
            curr_instrument = instruments[i]
            print("{},{}".format(curr_ticker,curr_instrument))
            print(get_quote_table(curr_ticker))
            q = {k:v for k,v in get_quote_table(curr_ticker).items() if k in info}
            q['ticker'] = curr_ticker
            q['_id'] = count
            q['instrument'] = curr_instrument
            q['datetime'] = now
            df = df.append(q,ignore_index=True)
        #rename
        df = df.rename(columns={'Quote Price':'quotePrice','Volume':'volume','Open':'open','Previous Close':'previousClose','PE Ratio (TTM)':'peRatio'})
        df=df.fillna(0)
        print(df)
        self.market_data.delete_many({})
        records = json.loads(df.T.to_json()).values()
        if (records):
            self.market_data.insert_many(records)
