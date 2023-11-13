from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import chromedriver_autoinstaller_fix

#安裝chrome webdriver
chromedriver_autoinstaller_fix.install()

# 利用WebDriver開啟網站
driver = webdriver.Chrome()
URL = 'https://www.ptt.cc/bbs/Education/index.html'

with open('Selenium_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # 定義 CSV 欄位
    fieldnames = ['日期', '作者', '標題', '網址']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 寫入 CSV 欄位名稱
    writer.writeheader()
    driver.get(URL) 

    # 開始爬取，以2頁為例
    for round in range(2):
        # 等待頁面刷新
        # driver.implicitly_wait(10)

        # 尋找需要的資料
        articles = driver.find_elements(By.CSS_SELECTOR, 'div.title a')
        author = driver.find_elements(By.CSS_SELECTOR, 'div.author')
        Date = driver.find_elements(By.CSS_SELECTOR, 'div.date')

        # 反轉列表
        articles.reverse()
        author.reverse()
        Date.reverse()

        # 把資料寫進CSV
        for x, auth, date in zip(articles, author, Date):
            writer.writerow({'標題': x.text, '網址': x.get_attribute('href'), '作者': auth.text, '日期': date.text})

        # 找到上頁的按鈕，按下去
        driver.find_element(By.CSS_SELECTOR, 'div.btn-group-paging a:nth-child(2)').click()


# 關閉chrome webdriver
driver.quit()
#driver.close()