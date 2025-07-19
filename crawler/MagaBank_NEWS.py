
import requests
import bs4 as bs
import pandas as pd
from datetime import datetime, timedelta
import tabulate
import jieba.analyse
import jieba
import logging
from crawler.worker import app
from crawler.mysqlcreate import upload_data_to_mysql_MagaBank_NEWS
import sys

@app.task()

def Bank_NEWS(news_date):
    jieba.setLogLevel(logging.WARNING)

    table = []
    h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    start_date = datetime.strptime(news_date, "%Y-%m-%d").date()
    end_date = datetime.today().date()
    current_date = start_date

    while current_date <= end_date:
        date_str = f"{current_date.year}-{current_date.month}-{current_date.day}"

        for page in range(1, 6):
            url = f"https://fund.megabank.com.tw/w/wp/wu01megaNews.djhtm?A=NA&B={date_str}&C=NA&Page={page}"
            response = requests.get(url, headers=h)
            html = bs.BeautifulSoup(response.text, features="html.parser")

            for tr in html.find_all('tr'):
                en_date = tr.find('td', class_=['wfb2c', 'wfb5c'])
                en_title = tr.find('a')

                if en_date and en_title:

                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%Y/%m/%d")

                    if en_date.text.strip() == formatted_date:
                        date_final = en_date.text.strip()
                        title_final = en_title.text.strip()
                        en_url = en_title['href']
                        url_final = "https://fund.megabank.com.tw" + en_url
                        tags = jieba.analyse.extract_tags(title_final)

                        data = {
                            "日期": date_final,
                            "標題": title_final,
                            "連結": url_final,
                            "標籤": tags
                        }
                        if data not in table:  # 加這行就能避免重複
                            table.append(data)

        current_date += timedelta(days=1)  # 換下一天
    
    df = pd.DataFrame(table)
    
    df["標籤"] = df["標籤"].apply(lambda x: ", ".join(x))

    df = df.rename(columns={"日期": "Date",
                            "標題": "Title",
                            "連結": "Link",
                            "標籤": "Label"})
    
    print("爬蟲完成")
    
    upload_data_to_mysql_MagaBank_NEWS(df)
    print("輸入進mysql完成")
    # df = pd.json_normalize(table)
    # print(tabulate.tabulate(df, headers='keys', tablefmt='grid'))

    
if __name__ == "__main__":
    news_date = sys.argv[1]
    print(f"✅ 進入 main，Bank_NEWS: {news_date}", flush=True)
    Bank_NEWS(news_date)
   