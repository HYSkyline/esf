# -*- coding:utf-8 -*-
__author__ = '双犬子'

import copy

print "Link Start!"

lis = [[u'一', '01'], [u'二', '02'], [u'三', '03'], [u'四', '04']]
# lis.append(['01', '02'])
# lis.append('00')
# lis.append(['01', '02', '03'])
# lis.append(['11', '12'])
# lis.append('01')
# lis.append(['11', '12', '13'])
# lis.append(['21', '22'])
# lis.append('02')
# lis.append(['21', '22', '23'])

print "list:"
print lis

# lis = ['1', '2', '3']

# dic = {}
# print lis[0][0]
dic = dict(lis)


print "dict:"
print dic

dic['31'] = '32'
print "dict:"
print dic

# print dic['11']


print "Link Logout."
