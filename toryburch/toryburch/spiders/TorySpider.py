# -*- coding: utf-8 -*-

import scrapy
import sys
# import re
from toryburch.items import ToryburchItem
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
reload(sys)
sys.setdefaultencoding('utf-8')

class TorySpider(scrapy.Spider):
    name = "toryburch"
    allowed_domains = ["toryburch.com"]
    start_urls = [
        "https://www.toryburch.com/handbags/clutches-evening-bags/?icampid=hb_p3",]

    def parse(self, response):
        hxs = Selector(response)
        selects = []
        selects = hxs.xpath('//ol[@typeof="BreadcrumbList"]')
        for sel in selects:
            cate = sel.xpath('li[@property="itemListElement"]/a/span/text()').extract()

        selects = []
        selects = hxs.xpath('//div[@class="producttile-inner"]')
        items = []
        # p = re.compile(r"^[+-]?\d*(\.?\d*)$")
        for sel in selects:
            item = ToryburchItem()
            name = sel.xpath('div[@class="name"]/a/@title').extract()
            standard_price = sel.xpath('div[@class="pricing"]/div[@class="price"]/div[@class="discountprice"]/div[@class="standardprice"]/text()').extract()
            sales_price = sel.xpath('div[@class="pricing"]/div[@class="price"]/div[@class="discountprice"]/div[@class="salesprice"]/text()').extract()
            no_sales_price = sel.xpath('div[@class="pricing"]/div[@class="price"]/div[@class="salesprice"]/text()').extract()
            desc = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div[@class="productimage with-alternate"]/a/img[@class="product-image-primary"]/@title').extract()
            url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div[@class="productimage with-alternate"]/a/@href').extract()
            img_url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div[@class="productimage with-alternate"]/a/img[@class="product-image-primary"]/@src').extract()

            if not standard_price:
                standard_price = no_sales_price
            if not sales_price:
                sales_price = ['$0',]

            item["name"] = name
            item["standard_price"] = standard_price
            item["sales_price"] = sales_price
            item["desc"] = desc
            item["url"] = url
            item["img_url"] = img_url
            # yield item
            items.append(item)
        return items

            # yield item

            # CREATE TABLE TORYBURCH(ROW_ID INTEGER PRIMARY KEY AUTOINCREMENT, CATEGORY VARCHAR(100), NAME VARCHAR(100), STANDARD_PRICE VARCHAR(100), SALES_PRICE VARCHAR(100), DESC VARCHAR(100), URL VARCHAR(100), IMG_URL VARCHAR(100), CREATED DATE, LAST_UPD DATE);
            # sql = "INSERT INTO TORY_HANDBAGS(NAME, STANDARD_PRICE, SALES_PRICE, DESC, URL, IMG_URL" \
            #       ", CREATED, LAST_UPD) VALUES (:NAME, :STANDARD_PRICE, :SALES_PRICE, :DESC" \
            #       ", :URL, :IMG_URL, DATETIME('NOW', 'LOCALTIME'), DATETIME('NOW', 'LOCALTIME'));"
            # cur.execute(sql, {"NAME":name[0], "STANDARD_PRICE":standard_price[0], "SALES_PRICE":sales_price[0], "DESC":desc[0], "URL":url[0], "IMG_URL":img_url[0]})
            # sql = "INSERT INTO TORY_HANDBAGS(NAME) VALUES (:NAME);"
            # cur.execute(sql, {"NAME": name[0]})
            # conn.commit()

        # conn.close()

            # scrapy crawl toryburch -o re.csv -t csv