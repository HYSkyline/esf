# coding:utf-8
__author__ = '双犬子'

import sys
import urllib2
from StringIO import StringIO
import gzip
import re
import pymongo

reload(sys)
sys.setdefaultencoding('UTF-8')

print "Link Start!"

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.mydb

communities_urls = ['http://jufuyuan025.fang.com/xiangqing/']
print "---file reading completed."

data = ""
try:
    req = urllib2.Request(communities_urls[0])
    response = urllib2.urlopen(req)
    if response.info().get('content-encoding') == 'gzip':           # 如果网页采用了gzip传输数据（通过返回的网页info属性判读）
        buf = StringIO(response.read())         # 以得到的网页源码模拟gzip文件形式
        f = gzip.GzipFile(fileobj=buf)          # 以gzip模块对网页源码进行解析
        data = f.read()         # 得到网页源码
        # print "-----------------The No." + str(i) + " page has been read by gzip."           # 确认第i页已经被gzip读取
    else:
        data = response.read()           # data采用正常的网页源码读取方式
        # print "-----------------The No." + str(i) + " page has been read."          # 确认第i也已经被正常读取
    print "---code reading completed."
except Exception as e:
    print "---code reading failed.(No.1 page attach failed.)"

name_search = '<span class="floatl">(.*?)</span>'
add_search = '<dd title=".*?"><strong>(.*?)</strong>(.*?)</dd>'
info_search = "<dd><strong>(.*?)</strong>(.*?)</dd>"
name = re.findall(name_search, data, re.S)
add = re.findall(add_search, data, re.S)
info = re.findall(info_search, data, re.S)
# add_dic = dict(add)
# info_dic = dict(info)

print "---data preparing completed."

lis_one_trans = []
try:
    for each in add:
        data01_trans = each[0].decode('GB2312').encode('UTF-8')
        data02_trans = each[1].decode('GB2312').encode('UTF-8')
        lis_data_trans = []
        lis_data_trans.append(data01_trans)
        lis_data_trans.append(data02_trans)
        lis_one_trans.append(lis_data_trans)
    add_dic = dict(lis_one_trans)

    for each in info:
        data01_trans = each[0].decode('GB2312').encode('UTF-8')
        data02_trans = each[1].decode('GB2312').encode('UTF-8')
        lis_data_trans = []
        lis_data_trans.append(data01_trans)
        lis_data_trans.append(data02_trans)
        lis_one_trans.append(lis_data_trans)
    info_dic = dict(lis_one_trans)

    info_dic.update(add_dic)
    name_trans = name[0].decode('GB2312').encode('UTF-8')
    info_dic['name'] = name_trans
    db.mytab.save(info_dic)
except Exception as e:
    print str(e)
finally:
    conn.close()

print "Link Logout."
