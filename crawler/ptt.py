
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
from crawler.worker import app
from crawler.mysqlcreate import upload_data_to_mysql_ptt

@app.task()

def PTT_news(start_index):
    def get_full_date(post_url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        cookies = {'over18': '1'}

        try:
            res = requests.get(post_url, headers=headers, cookies=cookies)
            soup = BeautifulSoup(res.text, "html.parser")
            meta_tags = soup.find_all("span", class_="article-meta-value")
            if len(meta_tags) >= 4:
                date_str = meta_tags[3].text.strip()  # e.g. 'Wed Jun 3 10:58:01 2020'
                date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                return date_obj.strftime("%Y/%m/%d")
        except:
            return "Unknown"

    def crawl_page(url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        cookies = {'over18': '1'}

        res = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.find_all("div", class_="r-ent")

        data_list = []

        for a in articles:
            title_div = a.find("div", class_="title")
            if title_div and title_div.a:
                title = title_div.a.text.strip()
                href = title_div.a['href']
                post_url = "https://www.ptt.cc" + href
                full_date = get_full_date(post_url)
            else:
                title = "沒標題"
                full_date = "Unknown"

            pop_div = a.find("div", class_="nrec")
            pop = pop_div.span.text.strip() if pop_div and pop_div.span else "None"

            data_list.append({
                "標題": title,
                "人氣": pop,
                "日期": full_date
            })

            time.sleep(0.5)  # small delay to avoid being blocked

        return data_list

    # === Set your page range ===
    def get_latest_index(board):
        url = "https://www.ptt.cc/bbs/" + board +"/index.html"
        res = requests.get(url, cookies={'over18': '1'})
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)
        a = soup.find_all("a", {"class" : "btn wide"})
        # print(a)
        href = a[1]["href"]
        split_href = href.split("/")
        latest_index = split_href[-1]

        delete_words = ["index", ".", "html"]

        for delete in delete_words:
            latest_index = latest_index.replace(delete, "")
        return int(latest_index) + 1 

    board = "stock"
   



    # start_index = 8950
    end_index =  get_latest_index(board)# For testing, small range first
    
    # ===========================

    base_url = "https://www.ptt.cc/bbs/Stock/index{}.html"
    all_data = []

    for i in range(start_index, end_index + 1):
        url = base_url.format(i)
        print(f"Crawling: {url}")
        try:
            data = crawl_page(url)
            all_data.extend(data)
            time.sleep(2.0)
        except Exception as e:
            print(f"⚠️ Error at {url}: {e}")
            continue

    df = pd.DataFrame(all_data)
    df = df.rename(columns={"標題": "Title",
                            "人氣": "Popularity",
                            "日期": "Date",
                            })
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df[df["Title"].notna()]
    df = df[df["Title"] != "沒標題"]
    df = df[df["Date"].notna()]
    # df['Date'] = df['Date'].apply(lambda x: None if pd.isna(x) else x)
    upload_data_to_mysql_ptt(df)
    print("✅ Done. Saved to ptt_stock_realdate.csv")