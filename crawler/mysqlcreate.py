import pandas as pd
import requests

from sqlalchemy import create_engine, text  # 建立資料庫連線的工具（SQLAlchemy）
from sqlalchemy import BigInteger, Column, Date, DateTime, Integer ,Float ,DECIMAL,VARCHAR, MetaData, String, Table
from sqlalchemy.dialects.mysql import (
    insert,
)  

from crawler.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT



def upload_data_to_mysql_cnyes_headlines(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database

    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    DB_name = "crawlerDB"
    with engine.connect() as conn:
        conn.execute (text(f"CREATE DATABASE IF NOT EXISTS {DB_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    address_db = f"{address}/{DB_name}"
    engine_db = create_engine(address_db)

    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(

        "cnyes_headlines",  # 資料表名稱
        metadata,
        Column("pub_time", DateTime, primary_key=True),  
        Column("Title", String(100), primary_key=True),
        Column("link", String(100)),

    )
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine_db)
    # 遍歷 DataFrame 的每一列資料
    for _, row in df.iterrows():
        # 使用 SQLAlchemy 的 insert 語句建立插入語法
        insert_stmt = insert(stock_price_table).values(**row.to_dict())

        # 加上 on_duplicate_key_update 的邏輯：
        # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{
                col.name: insert_stmt.inserted[col.name]
                for col in stock_price_table.columns
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine_db.begin() as conn:
            conn.execute(update_stmt)








def upload_data_to_mysql_ETF_historyprice(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
  
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    DB_name = "crawlerDB"
    with engine.connect() as conn:
        conn.execute (text(f"CREATE DATABASE IF NOT EXISTS {DB_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    address_db = f"{address}/{DB_name}"
    engine_db = create_engine(address_db)

    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(
        "ETF_historyprice",  # 資料表名稱
        metadata,
        Column("Date", Date, primary_key=True),
        Column("Stock_id", VARCHAR(50), primary_key=True),
        Column("Close", DECIMAL(5,2)), 
        Column("Adj_Close", DECIMAL(5,2)), 
        Column("Volume", Integer),  
    )   
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine_db)

    # 遍歷 DataFrame 的每一列資料
    for _, row in df.iterrows():
        # 使用 SQLAlchemy 的 insert 語句建立插入語法
        insert_stmt = insert(stock_price_table).values(**row.to_dict())

        # 加上 on_duplicate_key_update 的邏輯：
        # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{
                col.name: insert_stmt.inserted[col.name]
                for col in stock_price_table.columns
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine_db.begin() as conn:
            conn.execute(update_stmt)
    print("輸入進mysql完成")









def upload_data_to_mysql_ETF_PremiumDiscount(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
  
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    DB_name = "crawlerDB"
    with engine.connect() as conn:
        conn.execute (text(f"CREATE DATABASE IF NOT EXISTS {DB_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    address_db = f"{address}/{DB_name}"
    engine_db = create_engine(address_db)

    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(
        "ETF_PremiumDiscount",  # 資料表名稱
        metadata,
        Column("Date", Date, primary_key=True),
        Column("Stock_id",VARCHAR(50), primary_key=True),
        Column("Net_worth", Float), 
        Column("Market_Capitalization", Float), 
        Column("premium_discount_rate", String(10)),  
    )   
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine_db)
    # 遍歷 DataFrame 的每一列資料
    for _, row in df.iterrows():
        # 使用 SQLAlchemy 的 insert 語句建立插入語法
        insert_stmt = insert(stock_price_table).values(**row.to_dict())

        # 加上 on_duplicate_key_update 的邏輯：
        # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{
                col.name: insert_stmt.inserted[col.name]
                for col in stock_price_table.columns
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine_db.begin() as conn:
            conn.execute(update_stmt)




def upload_data_to_mysql_MagaBank_NEWS(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database

    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    DB_name = "crawlerDB"
    with engine.connect() as conn:
        conn.execute (text(f"CREATE DATABASE IF NOT EXISTS {DB_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    address_db = f"{address}/{DB_name}"
    engine_db = create_engine(address_db)

    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(
        "MagaBank_NEWS",  # 資料表名稱
        metadata,
        Column("Date", Date ),
        Column("Title", String(100), primary_key=True),
        Column("Link", String(100)), 
        Column("Label", String(100)),
    )
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine_db)

    # 遍歷 DataFrame 的每一列資料
    for _, row in df.iterrows():
        # 使用 SQLAlchemy 的 insert 語句建立插入語法
        insert_stmt = insert(stock_price_table).values(**row.to_dict())
        print(insert_stmt)
        # 加上 on_duplicate_key_update 的邏輯：
        # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{
                col.name: insert_stmt.inserted[col.name]
                for col in stock_price_table.columns
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine_db.begin() as conn:
            conn.execute(update_stmt)




def upload_data_to_mysql_ptt(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
  
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    DB_name = "crawlerDB"
    with engine.connect() as conn:
        conn.execute (text(f"CREATE DATABASE IF NOT EXISTS {DB_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    address_db = f"{address}/{DB_name}"
    engine_db = create_engine(address_db)

    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(
        "ptt",  # 資料表名稱
        metadata,
        Column("Date", Date ),
        Column("Title", String(100), primary_key=True),
        Column("Popularity", String(100)), 
    )
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine_db)

    # 遍歷 DataFrame 的每一列資料
    for _, row in df.iterrows():
        # 使用 SQLAlchemy 的 insert 語句建立插入語法
        insert_stmt = insert(stock_price_table).values(**row.to_dict())

        # 加上 on_duplicate_key_update 的邏輯：
        # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{
                col.name: insert_stmt.inserted[col.name]
                for col in stock_price_table.columns
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine_db.begin() as conn:
            conn.execute(update_stmt)





def upload_data_to_mysql_vix(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
   
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    DB_name = "crawlerDB"
    with engine.connect() as conn:
        conn.execute (text(f"CREATE DATABASE IF NOT EXISTS {DB_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    address_db = f"{address}/{DB_name}"
    engine_db = create_engine(address_db)

    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(
        "vix",  # 資料表名稱
        metadata,
        Column("Date", Date, primary_key=True),
        Column("Close", Float),  # 主鍵 stock_id 欄位
    )
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine_db)
    # 遍歷 DataFrame 的每一列資料
    for _, row in df.iterrows():
        # 使用 SQLAlchemy 的 insert 語句建立插入語法
        insert_stmt = insert(stock_price_table).values(**row.to_dict())

        # 加上 on_duplicate_key_update 的邏輯：
        # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
        update_stmt = insert_stmt.on_duplicate_key_update(
            **{
                col.name: insert_stmt.inserted[col.name]
                for col in stock_price_table.columns
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine_db.begin() as conn:
            conn.execute(update_stmt)



