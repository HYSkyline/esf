# -*- coding:utf-8 -*-
__author__ = '双犬子'

print "Link Start!"
f = open(r"F:\application\python\esftsts.txt", "r")
communities_urls = f.readlines()
# communities_urls = f.readline()
f.close()
print "---file reading completed."

f = open(r"F:\application\python\esftstss.txt", 'w')
for i in range(0, len(communities_urls)):
    print communities_urls[i+1]
    if ':' in communities_urls[i+1]:
        if communities_urls[i+1][6] == ":":
            percent = communities_urls[i+1][:7]
            communities_urls[i+1] = communities_urls[i+1][8:]
        else:
            percent = communities_urls[i+1][:4]
            communities_urls[i+1] = communities_urls[i+1][4:]
        f.writelines(communities_urls[i])
        f.write(percent)
        f.writelines('\n')

    # elif each[2] == "%":
    #     percent = each[:3]
    #     f.writelines(each[4:])
    #     f.writelines()
    #     f.writelines('\n')
    else:
        f.writelines(communities_urls[i])
        # f.writelines('\n')
f.close()
print "Link Logout."
