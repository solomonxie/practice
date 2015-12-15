# coding:utf-8

# === 使用MySQL数据库 ===
import MySQLdb

def sqlInsert(table='', titles='', values=[], sqlfile=''):
	'''
	# Function: 根据数据，生成批量Sql插入数据语句，并生成Mysql的.sql文件。
	# Params  : data=只接收List列表格式！！titles='列名1,列名2', data=[ [列值1,列值2], [列值1,列值2] ]
	# Notes   : 1.虽然标准SQL的批量插入语句中是用tuple元组格式，但是在这里会引发严重问题：
				"('hello')"在for循环中会被直接当作字符串处理而非tuple格式，就会变成['h','e','l','l','o']
				2.用repr()可以将数字1变成带引号的'1'....这个技巧其实很容易产生bug....
				3.data的嵌套格式不对，很有可能引发错误。所以必须遵守data的双重list[[1,2,3]]格式，而不能是[1,2,3]单重列表
	'''
	sqls = []
	for row in values:
		val = ['%d'%c if type(c)==int else '"%s"'%c for c in row]
		# for c in row: # 为每种数据类型添加引号
		# 	if type(c)==str: arr += str('"%s"'%c).encode('utf-8')
		# 	elif type(c)==int: arr += '%s'%c
		# val = ",".join(["%s"%repr(v.encode('utf-8')) for v in row]) if type(row)==list else repr(row.encode('utf-8'))
		sqls.append('INSERT INTO %s(%s) VALUES(%s);' %(table, titles, ','.join(val))) # 绝对不能用+=，否则会把每个字符认为一项
	# === 将SQL语句输出至文本文件中 ===
	outstring = '\n'.join(sqls)
	outstring = outstring.encode('utf-8') # 这一步编码是必不可少的-_-!
	if sqls and sqlfile: 
		with open(sqlfile, 'w') as f:
			# f.writelines([s+'\n' for s in sqls]) # 效率较低，但writelines()适合大量数据。
			f.write(outstring) # 比较正确，且适合少量数据
	return outstring if sqls else ''
def TEST_sqlInsert():
	titles = 'jobName,cmpName,feedback,workingAge,eduReq,cmpType,cmpSize,jobDescri,jobLink,cmpLink,jobPay,cmpLoc,jobUpdate'
	values = []
	values.append( [1,2,3,'test'] )
	values.append( [
		u'\u4e3b\u6570\u636e\u7ba1\u7406-\u6570\u636e\u7f16\u7801\u4eba\u5458', 
		u'\u5317\u4eac\u745e\u4fe1\u901a\u667a\u80fd\u6570\u636e\u6280\u672f\u6709\u9650\u516c\u53f8', 
		u'', 
		u'\u65e0\u7ecf\u9a8c', 
		u'\u5927\u4e13', 
		u'\u6c11\u8425', 
		u'20-99\u4eba', 
		u'1.\u4e13\u79d1\u4ee5\u4e0a\u5b66\u5386\uff0c\u673a\u68b0\u5de5\u7a0b\u53ca\u7535\u5b50\u4e13\u4e1a\u4f18\u5148\u3002  2.\u5177\u6709\u8e0f\u5b9e\u4e25\u8c28\u7684\u5de5\u4f5c\u4f5c\u98ce\uff0c\u8d23\u4efb\u5fc3\u5f3a\uff0c\u6709\u56e2\u961f\u5408\u4f5c\u610f\u8bc6\u3002      \u4efb\u804c\u8981\u6c42\uff1a  1.\u719f\u7ec3\u5e94\u7528OFFICE\u529e\u516c\u8f6f\u4ef6\u3002  2.\u6709', 
		u'http://jobs.zhaopin.com/424944712250018.htm', 
		u'http://company.zhaopin.com/CC424944712.htm', 
		u'\u9762\u8bae', 
		u'\u5317\u4eac', 
		u'12-15'
	] )
	sqlfile = ''
	sqlfile = './data/INSERT_INTO_TEMP_SEARCHRESULTS_ZHILIAN.sql'
	sqlInsert('TEMP_SEARCHRESULTS_ZHILIAN', titles=titles, values=values, sqlfile=sqlfile)

# -----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	TEST_sqlInsert()