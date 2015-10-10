# -*- coding:utf-8 -*-
__author__ = '双犬子'

import copy

print "Link Start!"

lis = []
lis.append(['01', '02'])
# lis.append('00')
# lis.append(['01', '02', '03'])
lis.append(['11', '12'])
# lis.append('01')
# lis.append(['11', '12', '13'])
lis.append(['21', '22'])
# lis.append('02')
# lis.append(['21', '22', '23'])

print "list:"
print lis

# lis = ['1', '2', '3']

dic = {}
dic = dict(lis)

print "dict:"
print dic

dic['31'] = '32'
print "dict:"
print dic

# print dic['11']


print "Link Logout."
