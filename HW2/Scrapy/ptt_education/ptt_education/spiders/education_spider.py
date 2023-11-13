# run with code in terminal : scrapy crawl education_spider -o Scrapy_data.csv
import scrapy
from ptt_education.items import PttEducationItem

class EducationSpider(scrapy.Spider):
    name = 'education_spider'
    start_urls = ['https://www.ptt.cc/bbs/Education/index.html']
    page_limit = 2  # 設定要爬取的頁數

    def parse(self, response):
        # 爬取所需資料
        articles = response.css('div.title a')
        authors = response.css('div.author')
        dates = response.css('div.date')

        # 反轉列表
        articles.reverse()
        authors.reverse()
        dates.reverse()

        for article, author, date in zip(articles, authors, dates):
            item = PttEducationItem()
            item['日期'] = date.css('::text').get()
            item['作者'] = author.css('::text').get()
            item['標題'] = article.css('::text').get()
            item['網址'] = response.urljoin(article.css('::attr(href)').get())

            yield item

        # 得到下一頁的網頁
        next_page = response.css('div.btn-group-paging a:nth-child(2)::attr(href)').get()
        if next_page and response.meta.get('page', 1) < self.page_limit:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse, meta={'page': response.meta.get('page', 1) + 1})
