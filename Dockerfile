# 使用 Ubuntu 20.04 作為基礎映像檔
FROM ubuntu:20.04

# 更新套件列表，並安裝 Python 3.8 以及 pip（Python 套件管理工具）
#-y 代表自動回答「yes」  &&：表示「上一個指令成功才執行下一個」，避免錯誤接續下去。

RUN apt-get update && \
    apt-get install python3.8 -y && \  
    apt-get install python3-pip -y

# 安裝特定版本的 pipenv（用於 Python 虛擬環境和依賴管理）
RUN pip install pipenv==2022.4.8

# 建立工作目錄 /crawler
#在映像檔中建立一個新的資料夾 /crawler，通常作為應用程式的主目錄。
#
RUN mkdir /All_crawler_storage_mysql

# 將當前目錄（與 Dockerfile 同層）所有內容複製到容器的 /crawler 資料夾
COPY . /All_crawler_storage_mysql/

# 設定容器的工作目錄為 /crawler，後續的指令都在這個目錄下執行
WORKDIR /All_crawler_storage_mysql/

# 根據 Pipfile.lock 安裝所有依賴（確保環境一致性）
# Pipfile.lock 是 由 Pipenv (pipenv lock) 自動產生的，你不應該手動編輯它。
# 根據 Pipfile 中的套件需求，解決所有相依套件，並產生或更新 Pipfile.lock。
# 必須先有一個 Pipfile，pipenv 才能根據它來產生 Pipfile.lock
# pip 是用來安裝套件的工具    env 是用來隔離 Python 執行環境的工具
# sync 是 synchronize  
RUN pipenv sync

# 設定語系環境變數，避免 Python 編碼問題
# ENV：用來在 Docker 映像裡設定環境變數，讓後續的程序都能讀到。
# LC_ALL 和 LANG 是 Linux 系統中控制**語言和區域設定（Locale）**的環境變數。
#C.UTF-8 是一個兼容 UTF-8 編碼的「C」語系區域設定，確保系統處理文字時支援 Unicode（UTF-8）編碼。

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# 啟動容器後，預設執行 bash（開啟終端）
# CMD 指定了容器啟動時預設要執行的命令。
# 這裡指定容器啟動後執行 /bin/bash，也就是打開一個 Bash 終端（shell）。
CMD ["/bin/bash"]
