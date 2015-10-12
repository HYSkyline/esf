# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import sys

reload(sys)
sys.setdefaultcoding = 'utf-8'


def http_check(lis):
    err_num = 0
    for ii in range(0, len(lis)):
        if lis[ii][:4] == "http":
            pass
        else:
            print lis[ii] + '--------' + str(ii)
            err_num += 1
    if err_num == 0:
        print "No http_error exists."
    return "Check finished."


def find_same(lis):
    unique = []
    for each in lis:
        if each in unique:
            pass
        else:
            unique.append(each)
    print "List Filter Finished."
    return unique

print "Link Start!"
f = open('f:\\application\\python\\coms.txt', 'r')
reads = f.readlines()
f.close()

fin = http_check(reads)
print fin

cor = find_same(reads)
print len(cor)
f = open('f:\\application\\python\\com.txt', 'w')
for each in cor:
    f.writelines(each)
f.close()
print "Link Logout."
