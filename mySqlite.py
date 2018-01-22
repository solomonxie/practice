# coding:utf8

import sqlite3
# 创建: 数据库/数据库连接/指针
cnet = sqlite3.connect('example.db')
cur  = cnet.cursor()
# 创建: 表格
cur.execute('CREATE TABLE IF NOT EXISTS test (seq REAL, content TEXT)')
# 插入: 一条数据
cur.execute('INSERT INTO test VALUES(1, "hello sqlite")')
# 更新: 插入的数据
cnet.commit() # 要用数据库连接来更新而不是用指针
cur.close()
cnet.close()
