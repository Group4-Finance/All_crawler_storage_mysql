
import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from crawler.mysqlcreate import upload_data_to_mysql_cnyes_headlines
import sys



from crawler.worker import app  # Celery app 引入

# Celery 任務註冊
@app.task()
def cnyes_headlines(month: str = "2025-07"):
    # 日期處理
    try:
        month_start = datetime.strptime(month, "%Y-%m")
    except ValueError:
        print(f"日期格式錯誤，請使用 yyyy-mm 格式，例如 '2020-01'")
        return

    month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    month_str = month_start.strftime("%Y-%m")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://news.cnyes.com/news/cat/headline"
    }

    def safe_request(url, headers, retry_delay_range=(60, 120), max_retries=5):
        for attempt in range(max_retries):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            elif response.status_code in [403, 429]:
                wait_time = random.randint(*retry_delay_range)
                print(f"遇到狀態碼 {response.status_code}，等待 {wait_time} 秒後重試（第 {attempt + 1} 次）")
                time.sleep(wait_time)
            else:
                print(f"收到非預期狀態碼：{response.status_code}，跳過此頁")
                return None
        print("多次重試失敗，跳過此頁")
        return None

    # 開始爬取每一天
    monthly_data = []
    date_ptr = month_start

    while date_ptr <= month_end:
        date_str = date_ptr.strftime("%Y-%m-%d")
        start_ts = int(date_ptr.timestamp())
        end_ts = int(date_ptr.replace(hour=23, minute=59, second=59).timestamp())

        print(f"開始抓取日期：{date_str}")
        page = 1

        while True:
            url = (
                f"https://api.cnyes.com/media/api/v1/newslist/category/headline"
                f"?startAt={start_ts}&endAt={end_ts}&limit=100&page={page}"
            )

            time.sleep(5)
            res = safe_request(url, headers)
            if not res:
                break

            try:
                data = res.json()
                items = data["items"]["data"]
            except Exception as e:
                print(f"解析失敗，第 {page} 頁跳過，錯誤：{e}")
                break

            if not items:
                break

            for item in items:
                timestamp = item["publishAt"]
                pub_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
                title = item["title"]
                news_id = item["newsId"]
                link = f"https://news.cnyes.com/news/id/{news_id}"
                monthly_data.append([pub_time, title, link])

            print(f"第 {page} 頁完成，當日累積：{len(monthly_data)} 筆")
            page += 1

        time.sleep(10)
        date_ptr += timedelta(days=1)

    monthly_df = pd.DataFrame(monthly_data, columns=["pub_time", "Title", "link"])

    upload_data_to_mysql_cnyes_headlines(monthly_df)


    filename = "mysql"


    print(f"{month_str} 完成，共儲存 {len(monthly_data)} 筆新聞到 {filename}")



if __name__ == "__main__":
    month = sys.argv[1]
    print(f"✅ 進入 main，cnyes_headlines: {month}", flush=True)
    cnyes_headlines(month)
