# git clone 
git clone https://github.com/Group4-Finance/All_crawler.git

# producer_multi_queue.py
參數自行設定  
ex :
    cnyes_headlines.s("2025-06").apply_async(queue="cnyes_headlines")

"2025-06"可以調整成想要開始爬的起始月

# docker-compose-producer-network.yml
image: kong567/testcrawler:0.0.2 
image可以改成自己的  

# docker-compose-worker-network.yml
總共有6個worker
分別是 crawler_cnyes_headlines、ETF_historyprice
       、PremiumDiscount、MagaBank_NEWS、 vix、PTT

hostname 只影響flower裡的worker名稱


volumes 儲存資料

volumes:

      - /home/delight/All_crawler:/All_crawler

      - /home/delight/All_crawler/crawler_data/vix_data:/All_crawler/data/vix

volumes:

      - 工作總目錄(目前clone的資料夾路徑):跟Dockerfile的WORKDIR同路徑

      - 要存放csv的資料夾路徑:儲存在container內csv的路徑

在執行任務之前，volume 掛載為主機的檔案優先，若掛上去 容器內該目錄會被主機目錄蓋過去，等於是在主機上執行，所以第一行的工作總目錄一定要是 clone 的資料夾路徑，避免執行 docker compose 時找不到檔案，或是在 hostname 下面加上 working_dir: /All_crawler 並把 volumes 第一行刪除

要存放csv的資料夾可以用createfolder.py建立
儲存在container內csv的路徑為 各別爬蟲python檔最後儲存csv的路徑

ex: 

(vix.py)

    vix_data.to_csv('/All_crawler/data/vix/vix_daily.csv')
    ('/All_crawler/data/vix/vix_daily.csv')為在容器內儲存的路徑

!!!!!!若要在自己的主機執行 要將前面這段路徑"/home/delight/"改成自己的!!!!!!

如果不確定路徑在terminal執行 pwd  (pwd = print working directory)

---------------------------------------------------------------------------
# 指令
# 建立 image
### 如果要push 要將這段"kong567"改成自己的dockerhub
docker build -f Dockerfile -t kong567/testcrawler:0.0.2 .


# push image 
docker push kong567/testcrawler:0.0.2


# docker compose啟動
docker compose -f <filename> up -d   

-f 為 file 找到指定的yml檔 要加.yml ; up 為啟動並建立 yml檔中定義的service ; -d 為啟動服務後背景執行

docker compose -f rabbitmq-network.yml up -d

docker compose -f docker-compose-worker-network.yml up -d

docker compose -f docker-compose-producer-network.yml up -d



# container name
### container name  = <project_name>-<service_name>-<index>

all_crawler-PremiumDiscount-1                                                                                    
all_crawler-crawler_cnyes_headlines-1                                                                                    
all_crawler-vix-1                                                                                    
all_crawler-MagaBank_NEWS-1                                                                            
all_crawler-PTT-1                                                                                   
all_crawler-ETF_historyprice-1 

all_crawler-producer_multi_queue-1

all_crawler-rabbitmq-network-1


# 查看 container 執行狀況

docker logs containername  # 直接加上上面的containername

docker logs -f containername

-f 為 follow  持續監控，監控後不想看可以Crl+C 不影響worker執行


# 停止 container 運行 
docker stop container_name

# 停止所有container
docker stop $(docker ps -aq)

docker ps -aq 為查詢所有容器的ID ; $()為替換命令將查詢到的結果替換上來

# 刪除所有container
docker rm $(docker ps -aq)

