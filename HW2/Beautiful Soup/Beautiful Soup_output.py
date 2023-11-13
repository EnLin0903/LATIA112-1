# HTTP Method: GET(), POST()
import requests as rq

# 導入 BeautifulSoup module: 解析 HTML 語法工具
from bs4 import BeautifulSoup as BS 

import csv

# 將 PTT Stock 存到 URL 變數中
URL = 'https://www.ptt.cc/bbs/Education/index460.html' 


with open('Beautiful_Soup_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # 定義 CSV 欄位
    fieldnames = ['日期', '作者', '標題', '網址']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 寫入 CSV 欄位名稱
    writer.writeheader()

    # 使用 for 迴圈將逐筆將標籤(tags)裡的 List 印出, 這裡取1頁
    for round in range(2):
    
        # Send get request to PTT Education
        RES = rq.get(URL) 

        # 將 HTML 網頁程式碼丟入 bs4 分析模組
        soup = BS(RES.text, 'html.parser') 

        # 查找標題文章的 html 元素。過濾出標籤名稱為'div'且 class 屬性為 title, 子標籤名稱為'a'，並反轉列表
        articles = soup.select('div.title a') 
        articles.reverse()

        # 查找文章的 html 元素。過濾出標籤名稱為'div'且 class 屬性為 author，並反轉列表
        author = soup.select('div.author')
        author.reverse()

        # 查找文章的 html 元素。過濾出標籤名稱為'div'且 class 屬性為 date，並反轉列表
        Date = soup.select('div.date')
        Date.reverse()

        # 取出'下一頁'元素
        paging = soup.select('div.btn-group-paging a') 

        # 將'下一頁'元素存到 next_URL 中
        next_URL = 'https://www.ptt.cc' + paging[1]['href'] 

        # for 迴圈帶入到下一頁的 URL 資訊
        URL = next_URL 

        # 建立抓資料的變數
        y = 0

        # 萃取文字出來: title, URL
        for x in articles: 
            writer.writerow({'標題': x.text, '網址': 'https://www.ptt.cc' + x['href'], '作者': author[y].text, '日期': Date[y].text})
            y = y + 1
