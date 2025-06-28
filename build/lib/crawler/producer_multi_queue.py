from crawler.crawler_cnyes_headlines  import cnyes_headlines
from crawler.ETF_historyprice import historyprice
from crawler.ETF_PremiumDiscount import PremiumDiscount
from crawler.vix import vix_data
from crawler.MagaBank_NEWS import Bank_NEWS
from crawler.ptt import PTT_news

cnyes_headlines.s("2025-06").apply_async(queue="cnyes_headlines")
print("send crawler_cnyes_headlines task to cnyes_headlines queue")

etf_list = ['00757.TW','0052.TW','00713.TW','00830.TW','00733.TW','00850.TW','00692.TW','0050.TW','00662.TW','00646.TW']

for tickers in etf_list:
     historyprice.s(tickers).apply_async(queue="historyprice")
     print("send ETF_historyprice task to historyprice queue")

etf = ['00757','0052','00713','00830','00733','00850','00692','0050','00662','00646']

for stockno in etf:
    PremiumDiscount.s(stockno).apply_async(queue="PremiumDiscount")
    print("send ETF_PremiumDiscount task to PremiumDiscount queue")


Bank_NEWS.s("2025-06-01").apply_async(queue = "MagaBank_NEWS")
print("send MagaBank_NEWS task to MagaBank_NEWS queue")


vix_data.s("^vix").apply_async(queue="VIX")
print("send vix task to VIX queue")

PTT_news.s(8967).apply_async(queue="PTT_news")
print("send ptt task to PTT_news queue")





