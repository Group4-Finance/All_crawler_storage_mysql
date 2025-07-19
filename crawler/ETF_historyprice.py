# === 1 ：匯入套件 ===


import yfinance as yf
import pandas as pd
import time
from loguru import logger
from datetime import datetime
from crawler.worker import app
from crawler.mysqlcreate import upload_data_to_mysql_ETF_historyprice
import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@app.task()

def historyprice(ticker) :
    print(f"ETF_historyprice.py 啟動，收到的 ticker 是：{sys.argv[1]}")
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
    df['Stock_id'] = ticker
    logger.info(df)
    logging.info("已完成爬蟲，準備寫入資料庫")
    upload_data_to_mysql_ETF_historyprice(df)
    logging.info("已寫入 MySQL")
    


if __name__ == "__main__":
    ticker = sys.argv[1]
    print(f"✅ 進入 main，historyprice: {ticker}", flush=True)
    historyprice(ticker)

# etf_list = ['00757.TW','0052.TW','00713.TW','00830.TW','00733.TW','00850.TW','00692.TW','0050.TW','00662.TW','00646.TW']

# for tickers in etf_list:
#     if __name__ == "__main__":
#         historyprice(tickers)
    