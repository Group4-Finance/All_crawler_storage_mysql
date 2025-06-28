# === 1 ：匯入套件 ===


import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from crawler.worker import app
from crawler.mysqlcreate import upload_data_to_mysql_ETF_historyprice

@app.task()

def historyprice(ticker) :

    # === 2 ：設定參數 ===
    start_date = '2020-01-01'
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    # === 3 ：下載資料（保留原始 Close 與 Adj Close）===
    time.sleep(5)  # 避免過於頻繁請求
    df = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)

    # 提取該股票對應的資料欄位（扁平化）
    df_single = df.xs(ticker, level='Ticker', axis=1)

    # 判斷是否包含 Adj Close 欄位
    has_adj = 'Adj Close' in df_single.columns

    # 顯示前 5 筆資料
    print("前五筆資料：")
    print(df_single.head())


    # 動態選擇欄位
    columns_to_save = ['Close', 'Volume']
    if has_adj:
        columns_to_save.insert(1, 'Adj Close')  # 加在 Close 後面

    df = df_single[columns_to_save].rename(columns={"Adj Close": "Adj_Close"})
    df = df.reset_index()
    upload_data_to_mysql_ETF_historyprice(df)
