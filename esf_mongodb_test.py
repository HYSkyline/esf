# -*- coding:utf-8 -*-
__author__ = '双犬子'

import pymongo

print "Link Start!"

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.testdb
dbdata = db.tabtest.find()
try:
    for each in dbdata:
        print each['Love']
except Exception as e:
    print u"输出失败" + str(e)
db.tabtest.save({'Love': u"浙", 'location': u"湖州"})
dbdata = db.tabtest.find()
try:
    for each in dbdata:
        print each
except Exception as e:
    print str(e)

conn.close()

print "Link Logout."
