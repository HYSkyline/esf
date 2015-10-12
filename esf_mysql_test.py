# -*- coding:utf-8 -*-

import MySQLdb

print "Link Start!"
conn = MySQLdb.Connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    db="test"
)
cursor = conn.cursor()
print "Link completed."

try:
    sql = "insert into tabtest(action,obj2) values('Hell','act')"
    cursor.execute(sql)
    conn.commit()
except Exception as e:
    conn.rollback()
    print "sql error."+str(e)
finally:
    cursor.close()
    conn.close()

print "Link Logout."
