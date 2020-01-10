## 檔案說明
    本專案用flask搭配Heroku伺服器部屬https web server,再用 /callback post路徑和line bot 做串接,以下為檔案說明
    Procfile:宣告多種程序的類型（執行的程式種類）的檔案
    app.py:主程式
    config.ini:設定檔
    function.py:自定義函數檔
    requirements.txt:已安裝模組名稱,根據 requirements.txt 列表安裝模組
    runtime.txt:告知python版本
    nlp資料夾:存放介接威聖電子股份有限公司API的檔案
    fileTemplates資料夾:存放word模板
    fileOutput資料夾:存放輸出檔案
    templates資料夾:存放html模板
    static資料夾:存放靜態檔案css、js等
## 建置步驟1(申請Heroku帳號):
    因為使用Heroku平台,所以要先到Heroku網站建立帳號
    Heroku網址:https://dashboard.heroku.com
## 建置步驟2(創建Heroku APP):
    heroku登入後首頁new>create new app 建置您自己的APP
## 建置步驟3(建立Line bot):
    網址:https://developers.line.biz/en/
    ine帳號登入> Providers>Create創造提供者
    Channel >Create a channel> Messaging API>依據欄位填值創出一個Bot
    Webhook settings 狀態打開
    並查出以下資訊
    Channel ID :
    Channel secret(沒有的話點選Issue):
    token:
    Webhook URL(https://{Heroku_app_name}.herokuapp.com/callback):
    Basic ID:

