# -*- coding:utf-8 -*-


import sys
import urllib
import urllib2
import re
from StringIO import StringIO
import gzip
import time
import pymongo

reload(sys)         # 重新运行sys模块，即重启程序运行环境
sys.setdefaultencoding('UTF-8')         # 强制设定程序在UTF-8环境中运行

t1 = time.time()            # 获取当前时间戳，用于程序总用时计算
print "Link Start!"         # 程序开始
num = 0         # 计数器，用以计算正确存储的数据个数
f = open(r"F:\application\python\com.txt", "r")         # 只读方式打开txt文件（内含多条目标URL）
communities_urls = f.readlines()            # 读取txt文件中的URL，至变量communities_urls
f.close()           # 关闭txt文件
print "--->file reading completed."         # 文件读取完成标志

conn = pymongo.MongoClient('127.0.0.1', 27017)          # 连接MongoDB服务器
db = conn.testdb            # 选择MongoDB服务器中的数据库
print "--->database attach completed."          # 数据库成功连接标志

for i in range(0, len(communities_urls)):           # 以i作为序数，对目标URL进行遍历
    # 读取网页源码
    try:
        req = urllib2.Request(communities_urls[i])          # 建立打开网页的请求
        response = urllib2.urlopen(req)         # 打开网页
        if response.info().get('content-encoding') == 'gzip':           # 如果网页采用了gzip传输数据（通过返回的网页info属性判读）
            buf = StringIO(response.read())         # 以得到的网页源码模拟gzip文件形式
            f = gzip.GzipFile(fileobj=buf)          # 以gzip模块对网页源码进行解析
            data = f.read()         # 得到网页源码
            # print "-----------------The No." + str(i) + " page has been read by gzip."           # 确认第i页已经被gzip读取
        else:
            data = response.read()           # data采用正常的网页源码读取方式
            # print "-----------------The No." + str(i) + " page has been read."          # 确认第i也已经被正常读取
        print "------>code reading completed."          # 网页源码成功读取标志
    except Exception as e:
        print "||||||code reading failed.(No." + str(i+1) + " page attach failed.)" + str(e)            # 网页源码读取失败标志
        continue
    # 正则匹配
    name_search = '<span class="floatl">(.*?)</span>'           # 对小区名称的正则表达式
    add_search = '<dd title=".*?"><strong>(.*?)</strong>(.*?)</dd>'         # 对小区部分属性的正则表达式
    info_search = "<dd><strong>(.*?)</strong>(.*?)</dd>"            # 对小区部分属性的正则表达式
    name = re.findall(name_search, data, re.S)          # 通过正则表达式查找小区名称
    add = re.findall(add_search, data, re.S)            # 通过正则表达式查找小区属性
    info = re.findall(info_search, data, re.S)          # 通过正则表达式查找小区属性
    print "------>item searching completed."            # 小区属性解析完成标志
    # 数据准备
    lis_one_trans = []          # 转码时的中间变量（此处通过人工合成新变量，实现对字典的整体转码）
    try:
        for each in add:
            data01_trans = each[0].decode('GB2312').encode('UTF-8')         # 此处可通过charter模块的detect方法查看字符串编码
            data02_trans = each[1].decode('GB2312').encode('UTF-8')
            lis_data_trans = []
            lis_data_trans.append(data01_trans)
            lis_data_trans.append(data02_trans)
            lis_one_trans.append(lis_data_trans)
        add_dic = dict(lis_one_trans)           # dict()函数通过对单个列表中的两项（只能存在两项）进行操作，合成字典

        for each in info:
            data01_trans = each[0].decode('GB2312').encode('UTF-8')
            data02_trans = each[1].decode('GB2312').encode('UTF-8')
            lis_data_trans = []
            lis_data_trans.append(data01_trans)
            lis_data_trans.append(data02_trans)
            lis_one_trans.append(lis_data_trans)
        info_dic = dict(lis_one_trans)

        info_dic.update(add_dic)            # 将add字典合并到info字典中
        name_trans = name[0].decode('GB2312').encode('UTF-8')           # 对小区名称进行转码
        info_dic['name'] = name_trans           # 将小区名称合并到info字典中
        print "------>data preparing completed."            # 字典转码完成标志
    except Exception as e:
        print "||||||No." + str(i + 1) + " item encoding transformation failed."            # 字典转码失败标志
        continue

    try:
        db.tabtest.save(info_dic)           # database插入数据，需要字典形式
        num += 1            # 成功保存后单项任务完成，计数器加1
        print "------>data writen to database completed."           # 保存完成标志
    except Exception as e:
        print "||||||MongoDB: No." + str(i + 1) + " item failed to save" + str(e)           # 保存失败标志

conn.close()            # 关闭MongoDB连接
t2 = time.time()            # 获取程序结束时的时间
time_cost = t2-t1           # 计算程序总用时
print '\n'          # 换行符
print "Link Report:"            # 输出连接报告
print "Usetime:" + str(time_cost) + "s"         # 执行时间长度
print "targets number:" + str(len(communities_urls))            # 总目标数
print "completed:" + str(num) + r"/failed:" + str(len(communities_urls)-num)            # 任务完成以及任务失败的个数
print "Link completed percent:" + str((num/len(communities_urls))*100) + r"%"           # 计算任务完成百分比
print '\n'          # 换行符
print "Link Logout."            # 任务结束，退出线程标志
