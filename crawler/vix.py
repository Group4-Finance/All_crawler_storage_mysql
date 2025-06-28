# install yfinance

import yfinance as yf
import pandas as pd
from datetime import datetime
from crawler.worker import app
from crawler.mysqlcreate import upload_data_to_mysql_vix

@app.task()


def vix_data(Volatility_Index):
    # ticker for the VIX
    vix_ticker = yf.Ticker(Volatility_Index)

    # Get today's date
    today = datetime.today().strftime('%Y-%m-%d')

    # Use the history method to fetch the data(DF)
    vix_data = vix_ticker.history(start="2020-01-01", end=today)

    # Resetting the index to have Date as a column
    vix_data = vix_data.reset_index()

    vix_data['Date'] = vix_data['Date'].dt.date

    # Round the Close prices to 2 decimal places
    vix_data['Close'] = vix_data['Close'].round(2)

    # Selecting columns
    vix_data = vix_data[['Date', 'Close']]

    upload_data_to_mysql_vix(vix_data)