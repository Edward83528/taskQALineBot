本專案用flask搭配Heroku伺服器部屬https的webServer,再用<b>/callback</b> post路徑和line bot 做串接,以下為本專案貢獻
* Q&A問答主要介接微軟Qnamaker和威聖電子API做介接
* 利用python docx-mailmerge模組填充事先處理好的WORD模板變數達到Line bot互動式填表
* 利用droxbox API2上傳檔案並回傳共連結，達到Line bot可以回傳word檔案功能
# 檔案說明
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
# 以下為建置步驟,下載本git專案並根據步驟1到6即可成功建置
## 建置步驟1(申請Heroku帳號):
    因為使用Heroku平台,所以要先到Heroku網站建立帳號
Heroku網址:<https://dashboard.heroku.com/>
## 建置步驟2(創建Heroku APP):
    heroku登入後首頁new>create new app 依照網頁步驟建置您自己的APP,並記住您自己的App名稱
## 建置步驟3(建立Line bot):
    到Line開發者網站建置Line bot
    網址:https://developers.line.biz/en/
    Line帳號登入> Providers>Create創造提供者
    Channel >Create a channel> Messaging API>依據欄位填值創出一個Bot
    Webhook settings 狀態打開並查出以下資訊
![image](https://github.com/harry83528/taskQALineBot/blob/master/messageImage_1578628507824.jpg)

*  Channel ID
*  Channel secret(沒有的話點選Issue)
*  token
*  Webhook URL(https://{Heroku_app_name}.herokuapp.com/callback)
*  Basic ID
## 建置步驟4(下載版更程式):
    安裝 Git與Heroku CLI
Git:<https://backlog.com/git-tutorial/tw/intro/intro2_1.html> <br>
Heroku CLI:<https://devcenter.heroku.com/articles/heroku-cli#windows>
## 建置步驟5(版更指令):
    下載本git專案到您的電腦,假設您下載路徑為D:\webapps\taskbot\
    安裝好後cmd Cd到上傳資料夾(專案資料夾)，並打以下指令
    D:\webapps\taskbot>
    $ heroku login
    $ git init
    $ heroku git:remote -a "Heroku APP名稱"
    上述步驟版更第一次才要做，當之後程式有修改，重做下列3個步驟就好
    $ git add .
    $ git commit -m "版更敘述文字"
    $ git push heroku master
    如果要重新clone下來的步驟:
    $ heroku login
    $ heroku git:clone -a "Heroku APP名稱"
    $ cd "Heroku APP名稱"
    錯誤想看log:
    $ heroku logs --tail
## 建置步驟6(Line Managerg刪除自動回覆機制):
    最後再到Line Manager頁面將Auto reply message資料全部刪除，這樣才可以將使用者送的訊息透過python後台處理，回丟訊息給使用者。
![image](https://github.com/harry83528/taskQALineBot/blob/master/messageImage_1578626946104.jpg)
# 重要程式碼解說
## 填充WORD模板變數
    要事先將word加入域的設定，加的方法如下：
    word打開>欲插入處ctrl+F9 反灰>並按右鍵>編輯功能變數>類別:合併列印/功能變數名稱:MergeField/欄位名稱:自定義變數名/格式:無>確定
```python
#word模板插入值(templatePath:模板路徑/outputPath:檔案輸出路徑/docClass:填充變數的類別)
def docMerge(templatePath,outputPath,docClass):
    template = templatePath
    # 建立郵件合併文件並檢視所有欄位
    document = MailMerge(template)
    print("Fields included in {}: {}".format(template,document.get_merge_fields()))
    #替換變數值
    document.merge(
    name= docClass.name,
    place=docClass.place
    )
    document.write(outputPath)
    uploaddFileName=str(datetime.datetime.now())+'.docx'
```
## Droxbox檔案上傳
```python
#將檔案上傳到Droxbox並回傳共享連結(path:將要上傳的檔案路徑/upload_name:上傳到drobox的檔名)
def put_file(path, upload_name):
    shareLink='';#drobox共享連結宣告
    TOKEN = config['Dropbox']['TOKEN']
    dbx = dropbox.Dropbox(TOKEN)
    dbx.users_get_current_account()
    with open(path, "rb") as f:
        dbx.files_upload(f.read(), "/{}".format(upload_name))　#上傳檔案
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings('/'+upload_name)　#開啟共享
        shareLink=shared_link_metadata.url　#共享連結
    return shareLink
```
## 微軟qnamaker介接
```python
#介接微軟qnamaker(message_text:line使用者鍵入文字)
def get_answer(message_text):
    url = config['Qnamaker']['url']
    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': config['Qnamaker']['Authorization']
                   }
               )
    data = response.json()
    try: 
        #我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        #這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']
        return answer
    except Exception:
        return "不好意思，系統發生錯誤，請稍後再試"
```
# reference
* https://medium.com/@zaoldyeck/%E5%88%A9%E7%94%A8-olami-open-api-%E7%82%BA-chatbot-%E5%A2%9E%E5%8A%A0-nlp-%E5%8A%9F%E8%83%BD-e6b37940913d?
* https://medium.com/@skywalker0803r/%E6%A5%B5%E9%80%9F%E6%90%AD%E5%BB%BA%E4%B8%80%E5%80%8B%E5%9F%BA%E6%9C%AC%E7%9A%84%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BAlinebot-python-qnamaker-ngrok-ddd757fbbedf
* https://www.dropbox.com/developers/documentation/http/overview
* https://www.itread01.com/content/1548054189.html
