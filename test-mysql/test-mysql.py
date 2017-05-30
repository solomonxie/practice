# coding:utf-8
import MySQLdb

def test_mysql_1(): # 测试基本的数据库连接
	db = MySQLdb.connect('localhost', 'root', '123123', 'test') # 打开数据库连接
	#                        ^本地     ^用户名  ^密码    ^数据库名
	# print type(db) # <class 'MySQLdb.connections.Connection'>
	cursor = db.cursor() # OK === 使用cursor()方法获取操作游标 
	# print type(cursor) # <class 'MySQLdb.cursors.Cursor'>
	cursor.execute('select version()') # OK === 使用execute方法执行SQL语句
	# n = cursor.execute('select version()') 会返回执行的记录数
	data = cursor.fetchone() # OK === Fetch One，获取一条数据 显示 -> '5.7.9-log'
	print 'Database version is %s' %data # 返回：Database version is 5.7.9-log
	db.close() # OK === 关闭数据库
	# print db # OK === 关闭后，它还是存在的。

def test_mysql_2(): # 测试基本的表查询
	db = MySQLdb.connect('localhost', 'root', '123123', 'world')
	cursor = db.cursor()
	# cursor.execute('drop table if exists employee') # OK === 删除某已存在的表
	cursor.execute('select * from city')
	results = cursor.fetchone() # 只返回指针所在的一条数据
	# print type(results) # <type 'tuple'>
	for col in results:
		print col
	results = cursor.fetchall() # 返回指针所在及之后的所有数据——指针移动了！
	# print type(results) # <type 'tuple'>
	for row in results: # fetchall()返回的是T
		# print len(row)
		for col in row:
			print col
		break
	db.close()

def test_mysql_3(): # 测试基本的数据插入
	db = MySQLdb.connect(host='localhost', user='root', passwd='123123', db='test', charset='')
	cursor = db.cursor()
	# sql = 'insert into tbtest (text) values ("what?")' # OK
	sql = 'insert into tbtest (text) values ("中文！")' # Failed === 到数据里就变成乱码了
	# sql = 'insert into tbtest (text) values (u"中文！")' # Failed === 不支持unicode插入
	# sql = 'insert into tbtest (text) values ("中文！")'.decode('utf-8').encode('utf-8') # Failed === 还是乱码
	cursor.execute(sql)
	db.commit()
	db.close()
	print 'ok'

def test_mysql_4(): # 测试中文乱码的解决
	# Method 1: setdefaultencoding()
	# import sys
	# reload(sys)
	# sys.setdefaultencoding('utf-8')

	# Method 2: connect(charset=utf8) # 注：这里必须是'utf8'，而不是'utf-8'
	db = MySQLdb.connect(host='localhost', db='test', user='root',passwd='123123', charset='utf8') 
	# cursor = db.cursor() 
	# # Method 3: list格式的unicode字符    ======= OK 只要是[]列表，无所谓Unicode还是普通字符
	# value = u"中文测试 Unicode, charset='utf8'"
	# print value
	# n = cursor.execute('insert into test(txt) values(%s) ',value)
	# db.commit()
	# db.close()
	# print n

	# Method 4: 在Python代码中设置访问数据库编码为UTF-8 
	cursor = db.cursor() 
	# cursor.execute("SET NAMES 'utf8'") 
	# cursor.execute("SET CHARACTER_SET_CLIENT=utf8") 
	# cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
	cursor.execute('insert into test(txt) values("我是中文") ') # OK 测试成功
	# cursor.execute('insert into test(txt) values("我是中文2，看看会不会保存设置。") ') # OK 第二次不写以上三条也通过
	# cursor.execute('insert into test(txt) values("我是中文3，看看不带charset=管不管用。") ') # Failed 无论怎么玩，charset=不设置就不通过
	# cursor.execute('insert into test(txt) values("我是中文4") ') # OK 测试成功
	cursor.execute('insert into test(txt) values("我是中文5，看看关了mysql终端，还会不会保留设置。") ') # OK 测试成功
	db.commit()
	db.close()

def test():
	data = [['jobName','cmpName','feedback','workingAge','eduReq','cmpType','cmpSize','jobDescri','jobLink','cmpLink','jobPay','cmpLoc','jobUpdate']]
	print repr(data[0])

# ====================================================
if __name__ == '__main__':
	test_mysql_4()
	# test()