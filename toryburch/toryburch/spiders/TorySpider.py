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
        cate = []
        for sel in selects:
            cate = sel.xpath('li[@property="itemListElement"]/a/span/text()').extract()
        category = ">".join(cate)
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

            item["category"] = category
            item["name"] = name
            item["standard_price"] = standard_price
            item["sales_price"] = sales_price
            item["desc"] = desc
            item["url"] = url
            item["img_url"] = img_url
            # yield item
            items.append(item)
        return items
