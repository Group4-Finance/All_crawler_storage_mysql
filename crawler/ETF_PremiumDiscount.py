import urllib.request as req
import pandas as pd
import datetime
from crawler.worker import app
from crawler.mysqlcreate import upload_data_to_mysql_ETF_PremiumDiscount
import sys

@app.task() 

def  PremiumDiscount(etf_list):
# 抓取每一個ETF的折溢價
    
    # 設定起始日期
    start_date = '2020-1-1'

    # 取得今天日期並轉為字串
    end_date = datetime.date.today().strftime('%Y-%m-%d')

    # MoneyDJ
    base_url_MoneyDJ = "https://www.moneydj.com/ETF/X/xdjbcd/Basic0003BCD.xdjbcd?etfid={}.TW&b={}&c={}"

    #url_MoneyDJ
    url_MoneyDJ = base_url_MoneyDJ.format(etf_list, start_date, end_date)

    response_MoneyDJ = req.urlopen(url_MoneyDJ)
    content_MoneyDJ = response_MoneyDJ.read().decode('utf-8')

    # 將內容按行分割
    lines = content_MoneyDJ.strip().split(' ')  # 分成 3 行
    dates = lines[0].split(',')
    navs = lines[1].split(',')
    prices = lines[2].split(',')

    # 組成表格資料
    records = []
    for date, nav, price in zip(dates, navs, prices ):
        records.append([date, float(nav), float(price)])

    # 建立 DataFrame
    df_MoneyDJ = pd.DataFrame(records, columns=['交易日期', '淨值', '市價'])
    df_MoneyDJ['交易日期'] = pd.to_datetime(df_MoneyDJ['交易日期'], format='%Y%m%d')

    # 計算折溢價利率（公式： (市價 - 淨值) / 淨值 ）
    df_MoneyDJ['折溢價利率(%)'] = ((df_MoneyDJ['市價'] - df_MoneyDJ['淨值']) / df_MoneyDJ['淨值'] * 100).map(lambda x: f"{x:.2f}%")
    
    df_MoneyDJ = df_MoneyDJ.rename(columns={"交易日期": "Date",
                                            "淨值": "Net_worth",
                                            "市價": "Market_Capitalization",
                                            "折溢價利率(%)": "premium_discount_rate"})
    df_MoneyDJ['Stock_id'] = etf_list 
    print("爬蟲完成")
    upload_data_to_mysql_ETF_PremiumDiscount(df_MoneyDJ)
    print("輸入進mysql完成")


if __name__ == "__main__":
    etf_list = sys.argv[1]
    print(f"✅ 進入 main，PremiumDiscount: {etf_list}", flush=True)
    PremiumDiscount(etf_list)