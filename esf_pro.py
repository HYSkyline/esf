# -*- coding:utf-8 -*-
__author__ = '双犬子'

import urllib
import urllib2
import re
from StringIO import StringIO
import gzip
import time

# def gzip_response(response):
#     if response.info().get('content-encoding') == 'gzip':           # 如果网页采用了gzip传输数据（通过返回的网页info属性判读）
#         buf = StringIO(response.read())         # 以得到的网页源码模拟gzip文件形式
#         f = gzip.GzipFile(fileobj=buf)          # 以gzip模块对网页源码进行解析
#         data = f.read()         # 得到网页源码
#         print "-----------------The No." + str(i) + " page has been read by gzip."           # 确认第i页已经被gzip读取
#         return data
    # else:
    #     data = response.read()           # data采用正常的网页源码读取方式
    #     print "-----------------The No." + str(i) + " page has been read."          # 确认第i也已经被正常读取
        # return data

t1 = time.time()
print "Link Start!"
num = 0
f = open(r"F:\application\python\comlite.txt", "r")
communities_urls = f.readlines()
# communities_urls = f.readline()
f.close()
print "---file reading completed."

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
        print "---code reading completed."
    except:
        print "---code reading failed.(No." + str(i+1) + " page attach failed.)"
        continue
    # 正则匹配
    name_search = '<span class="floatl">(.*?)</span>'
    add_search = '<dd title=".*?"><strong>(.*?)</strong>(.*?)</dd>'
    info_search = "<dd><strong>(.*?)</strong>(.*?)</dd>"
    name = re.findall(name_search, data, re.S)
    add = re.findall(add_search, data, re.S)
    info = re.findall(info_search, data, re.S)
    print "---item searching completed."
    # 写入文件
    add_dic = dict(add)
    info_dic = dict(info)
    info_dic.update(add_dic)
    f = open(r"F:\application\python\esftst.txt", 'a')
    try:
        f.writelines("address\n")
        for each in add:
            f.writelines(each)
            f.writelines('\n')
        # f.writelines('\n')
        f.writelines('\n')
        # f.writelines(name[0])
        # f.writelines(' ')
    except:
        print "No." + str(i + 1) + " item analyse failed(name Ref value address)."
        continue
    # try:
    #     f.writelines(add[0])
    #     f.writelines(' ')
    # except:
    #     print "No." + str(i + 1) + " item analyse failed(address)."
    #     continue
    f.writelines("information\n")
    for each in info:
        f.writelines(each)
        f.writelines('\n')
        # if "%" in each:
        #     f.writelines(each)
        #     f.writelines(' ')
        #     break
    f.writelines(time.strftime('%H:%M:%S', time.localtime()))
    f.writelines('\n')
    f.close()
    print "---file writing completed."
    num += 1
    print "No." + str(i + 1) + " item has been analysed."

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
