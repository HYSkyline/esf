# -*- coding:utf-8 -*-


import sys
import urllib
import urllib2
import re
from StringIO import StringIO
import gzip
import time
import pymongo

reload(sys)
sys.setdefaultencoding('UTF-8')

t1 = time.time()
print "Link Start!"
num = 0
f = open(r"F:\application\python\com.txt", "r")
communities_urls = f.readlines()

f.close()
print "--->file reading completed."

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.testdb
print "--->database attach completed."

for i in range(0, len(communities_urls)):
    # 读取网页源码
    try:
        req = urllib2.Request(communities_urls[i])
        response = urllib2.urlopen(req)
        if response.info().get('content-encoding') == 'gzip':           # 如果网页采用了gzip传输数据（通过返回的网页info属性判读）
            buf = StringIO(response.read())         # 以得到的网页源码模拟gzip文件形式
            f = gzip.GzipFile(fileobj=buf)          # 以gzip模块对网页源码进行解析
            data = f.read()         # 得到网页源码
            # print "-----------------The No." + str(i) + " page has been read by gzip."           # 确认第i页已经被gzip读取
        else:
            data = response.read()           # data采用正常的网页源码读取方式
            # print "-----------------The No." + str(i) + " page has been read."          # 确认第i也已经被正常读取
        print "------>code reading completed."
    except Exception as e:
        print "||||||code reading failed.(No." + str(i+1) + " page attach failed.)" + str(e)
        continue
    # 正则匹配
    name_search = '<span class="floatl">(.*?)</span>'
    add_search = '<dd title=".*?"><strong>(.*?)</strong>(.*?)</dd>'
    info_search = "<dd><strong>(.*?)</strong>(.*?)</dd>"
    name = re.findall(name_search, data, re.S)
    add = re.findall(add_search, data, re.S)
    info = re.findall(info_search, data, re.S)
    print "------>item searching completed."
    # 数据准备
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
        print "------>data preparing completed."
    except Exception as e:
        print "||||||No." + str(i + 1) + " item encoding transformation failed."
        continue

    try:
        db.tabtest.save(info_dic)
        num += 1
        print "------>data writen to database completed."
    except Exception as e:
        print "||||||MongoDB: No." + str(i + 1) + " item failed to save" + str(e)

conn.close()
t2 = time.time()
time_cost = t2-t1
print '\n'
print "Link Report:"
print "Usetime:" + str(time_cost) + "s"
print "targets number:" + str(len(communities_urls))
print "completed:" + str(num) + r"/failed:" + str(len(communities_urls)-num)
print "Link completed percent:" + str((num/len(communities_urls))*100) + r"%"
print '\n'
print "Link Logout."
