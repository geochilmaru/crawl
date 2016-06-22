# -*- coding: utf-8 -*-

import scrapy
import sys
# import re
from toryburch.items import ToryburchItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
reload(sys)
sys.setdefaultencoding('utf-8')

class TorySpider(scrapy.Spider):
    name = "toryburch"
    allowed_domains = ["toryburch.com"]
    start_urls = [
        "https://www.toryburch.com/handbags/clutches-evening-bags/",
        # "https://www.toryburch.com/handbags/clutches-evening-bags/?icampid=hb_p3",
        # "https://www.toryburch.com/robinson-convertible-shoulder-bag/28846.html?cgid=handbags-clutches&dwvar_28846_color=001&start=1",
        ]

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     # Rule(LinkExtractor(allow=('', ), deny=('.*\.html.*', )), callback='parse_detail', follow = True),
    #
    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     # Rule(LinkExtractor(allow=('.*\.html.*', ))),
    # )


    def parse(self, response):
        hxs = Selector(response)
        selects = []
        selects = hxs.xpath('//ol[@typeof="BreadcrumbList"]')
        cate = []
        cate_url = ""
        for index in range(len(selects)):
            cate = selects[index].xpath('li[@property="itemListElement"]/a/span/text()').extract()
            cate_url = selects[index].xpath('li[@property="itemListElement"]/a/@href').extract()
        category = "> ".join(cate)
        category_url = cate_url.pop()
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
            desc = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="product-image-primary"]/@title').extract()
            url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/@href').extract()
            img_url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="product-image-primary"]/@src').extract()
            alt_img_url = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="alternateimage"]/@src').extract()
            alt_img_desc = sel.xpath('div[@class="image"]/div[@class="thumbnail"]/div/a/img[@class="alternateimage"]/@alt').extract()

            if not standard_price:
                standard_price = no_sales_price
            if not sales_price:
                sales_price = ['$0',]

            item["category"] = category
            item["category_url"] = category_url
            item["name"] = name
            item["standard_price"] = standard_price
            item["sales_price"] = sales_price
            item["desc"] = desc
            item["url"] = url
            item["img_url"] = img_url
            item["alt_img_url"] = alt_img_url
            item["alt_img_desc"] = alt_img_desc
            yield Request(url[0], callback=self.parse_detail, meta={"item":item})
            # print "hello", item["style_num"]
            # print "world", item["style_num"]
            # items.append(item)
        # return items
            # print self.parse_detail(response)
        #
        #     # cleaned_url = "%s/?1" % url if not '/' in url.partition('//')[2] else "%s?1" % url
        #     # yield Request(cleaned_url, callback = self.parse_page, meta=meta,)
        #     yield item


    def parse_detail(self, response):
        item = response.meta['item']
        hxs = Selector(response)
        selects = []
        selects = hxs.xpath('//ul[@class="swatchesdisplay"]/li')
        color = []
        for sel in selects:
            col_attr = {}
            col = sel.xpath('a/span/text()').extract()
            img_url = sel.xpath('a/img[@class="swatchimage"]/@src').extract()
            col_code = sel.xpath('div/text()').extract()
            col_attr["color"] = col[0]
            col_attr["img_url"] = img_url[0]
            col_attr["col_code"] = col_code[0]
            color.append(col_attr)
        item["color"] = color
        # print item["color"]
        yield item
        # print item["name"], item["color"]
        # selects = []
        # selects = hxs.xpath('//div[@class="detailsPanel"]')
        # for sel in selects:
        #     desc = sel.xpath('div/ul/li/text()').extract()
        # spec = "<br>".join(desc)
        # item["spec"] = spec
        # item["color"] = color


        # detail = ['28846',]
        # item = []
        # item["hello"] = 'world'
        # return item
        # print item["name"], item["color"]
        # print "!!!!!"
        # yield "!!!!!"