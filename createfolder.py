import os


folder_path = '/home/delight/All_crawler/crawler_data'  

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    

folders = ["crawler_data/crawler_cnyes_headlines_data", "crawler_data/ETF_historyprice_data", 
           "crawler_data/ETF_PremiumDiscount_data", "crawler_data/MagaBank_NEWS_data", 
           "crawler_data/ptt_data", "crawler_data/vix_data" ]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)