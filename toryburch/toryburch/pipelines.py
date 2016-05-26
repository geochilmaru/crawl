# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import sys
import datetime
import logging
import sqlite3
from scrapy.exceptions import DropItem
from toryburch.items import ToryburchItem

class ToryburchPipeline(object):
    def __init__(self):
        try:
            self.conn = sqlite3.connect("./db/toryburch.db")
            self.conn.text_factory = str
            self.cursor = self.conn.cursor()
        except sqlite3.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

    def process_item(self, item, spider):
        # return item
        sql_sel = "SELECT * FROM TORYBURCH WHERE NAME = :DESC"
        # print "SELECT * FROM TORY_HANDBAGS WHERE NAME = %s" % str(item['name'][0].encode('utf-8'))
        self.cursor.execute(sql_sel, {"DESC":str(item['desc'][0].encode('utf-8'))})
        result = self.cursor.fetchone()

        if result:
            # print "data already exist"
            pass
        else:
            try:
                sql = "INSERT INTO TORYBURCH(NAME, STANDARD_PRICE, SALES_PRICE, DESC, URL, IMG_URL" \
                      ", CREATED, LAST_UPD) VALUES (:NAME, :STANDARD_PRICE, :SALES_PRICE, :DESC" \
                      ", :URL, :IMG_URL, DATETIME('NOW', 'LOCALTIME'), DATETIME('NOW', 'LOCALTIME'));"
                self.cursor.execute(sql, {"NAME":str(item['name'][0].encode('utf-8'))
                    , "STANDARD_PRICE":str(item['standard_price'][0].encode('utf-8'))
                    , "SALES_PRICE":str(item['sales_price'][0].encode('utf-8'))
                    , "DESC":str(item['desc'][0].encode('utf-8'))
                    , "URL":str(item['url'][0].encode('utf-8'))
                    , "IMG_URL":str(item['img_url'][0].encode('utf-8'))
                                  })
                self.conn.commit()
            except sqlite3.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                return item
