from flask import Flask
import Scrapper
import sys
import pandas as pd
import schedule
import threading

app = Flask(__name__)

def scrape(ticker_list):
    s = Scrapper.Scrapper()
    schedule.every(1).hour.do(s.scrape,ticker_list)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    csv_file = sys.argv[1]
    ticker_list = pd.read_csv(csv_file)['Ticker'].to_numpy()
    print(ticker_list)
    x = threading.Thread(target=scrape, args=[ticker_list])
    x.start()
    app.run(host='0.0.0.0')