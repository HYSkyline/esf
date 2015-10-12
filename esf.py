# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import urllib
import urllib2
import re
import sys
from StringIO import StringIO
import gzip
import time

reload(sys)         # 重新加载sys模块，准备改变编码
sys.setdefaultencoding（'utf-8'）            # 重新指定程序编码形式为utf-8
ff = open('F:\\application\\python\\communitesurl.txt', 'a')            # 创建文本文档，准备写入数据
print "Link Start!"         # 开始链接！

t1 = time.time()            # 获取程序开始运行时的时间戳，用于程序总运行时间的计算
num = 0         # 计数抓取到的总数据条数（包含失败数据）
error_num = 0           # 计数抓取失败的数据条数

for i in range(0, 101):         # 共有一百页的租售房信息网页，对其进行遍历抓取
    start_url = 'http://esf.nanjing.fang.com/house-a0265/i3'+str(i)         # 构建每一页的网页地址
    req = urllib2.Request(start_url)            # 创建读取网页的请求
    post_data = {
        'user-agent':'mozilla/5.0 (windows nt 10.0; wow64) applewebkit/537.36 (khtml, like gecko) chrome/45.0.2454.101 safari/537.36'
    }           # 设置请求的头文件草稿，模拟浏览器动作
    postdata = urllib.urlencode(post_data)          # 对头文件草稿进行编码，形成正式的头文件
    req.add_header('accept-encoding', 'gzip')           # 在读取网页的请求中加入头文件
    response = urllib2.urlopen(req, data=postdata)          # 发送头文件，读取网页
    if response.info().get('content-encoding') == 'gzip':           # 如果网页采用了gzip传输数据（通过返回的网页info属性判读）
        buf = StringIO(response.read())         # 以得到的网页源码模拟gzip文件形式
        f = gzip.GzipFile(fileobj=buf)          # 以gzip模块对网页源码进行解析
        data = f.read()         # 得到网页源码
        print "-----------------The No." + str(i) + " page has been read by gzip."           # 确认第i页已经被gzip读取
    else:
        data = response.read()           # data采用正常的网页源码读取方式
        print "-----------------The No." + str(i) + " page has been read."          # 确认第i也已经被正常读取

    sell_urls = []          # 创建各个租售房网页的存储列表
    sell_url_search = '<p class="title"><a href="(.*?)"  target="_blank" title="'           # 各个分网页的正则表达式
    sell_url = re.findall(sell_url_search, data, re.S)          # 以正则表达式读取分网页的地址
    for each in sell_url:           # 按每一页的租售房分网页来循环
        sell_urls.append('http://esf.nanjing.fang.com/'+each)           # 将各个分网页的url地址写入存储列表
    print "-----------------The No." + str(i) + " page has been analyzed"           # 确认分网页地址写入完成

    communities = []            # 创建存储社区详情url的列表
    for com_i in range(0, len(sell_urls)):          # com_i为计数项，按租售房分网页地址进行循环
        # time.sleep(5)         # 设置二级延时
        req = urllib2.Request(sell_urls[com_i])         # 创建读取请求
        req.add_header('accept-encoding', 'gzip')           # 增加请求内容
        response = urllib2.urlopen(req, data=postdata)          # 读取网页
        if response.info().get('content-encoding') == 'gzip':           # 如果网页采用了gzip传输数据（通过返回的网页info属性判读）
            buf = StringIO(response.read())         # 以得到的网页源码模拟gzip文件形式
            f = gzip.GzipFile(fileobj=buf)          # 以gzip模块对网页源码进行解析
            data = f.read()         # 得到网页源码
        else:
            data = response.read()           # data采用正常的网页源码读取方式

        com_search = '<span class="gray6">.*?</span>.*?&nbsp;&nbsp;<a id=".*?" href="(.*?)" target="_blank">.*?&gt;&gt;</a></dt>'
        # 各个社区详情网页的正则表达式
        com = re.findall(com_search, data, re.S)            # 以正则表达式读取社区详情网页的地址
        try:            # 可能会引发远程服务器封锁IP，进而报错使程序崩溃，因此使用try方法
            communities.append(com[0] + 'xiangqing/')           # 创建正式的社区详情网页的地址，写入存储列表
            print "The No." + str(com_i+1) + " item of No." + str(i) + " page has been detected"            # 确认社区详情网页已被读取
        except:
            print "The No." + str(com_i+1) + " item of No." + str(i) + " page detection failed---"          # 确认远程服务器已封锁端口，社区详情网页地址获取失败
            error_num += 1          # 失败次数加1
        num += 1            # 总计数加1

    for each in communities:            # 按社区详情网页列表循环，开始写入文件
        ff.writelines(each)         # 写入社区详情网页地址
        ff.writelines('\n')         # 换行符
    print "-----------------The No." + str(i) + " page has been finished"           # 确认第i页所有社区详情网页地址已经提取完成

ff.close()          # 关闭文本文档

t2 = time.time()            # 获取程序结束时的时间戳
time_cost = t2-t1           # 计算程序运行的总时长，单位为秒

print '\n'          # 换行
print "Mission Evaluate:"           # 任务总体评估
print "Mission has run for " + str(time_cost) + " seconds"          # 输出任务运行总时长
print str(num) + "records has been detected."           # 输出所有可抓取的数据总数
print str(num - error_num) + " records has been writen successfully."           # 输出成功获取的数据总数
print str(error_num) + " records has failed to be writen."          # 输出获取失败的数据总数
print '\n'          # 换行
print "Link Logout."            # 确认链接结束
