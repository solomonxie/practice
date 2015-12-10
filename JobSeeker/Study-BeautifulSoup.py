# -*- coding: utf-8 -*-
'''
	# Author    : Solomon Xie
	# Usage     : 测试BeautifulSoup一些用法及容易出bug的地方
	# Enviroment: Python 2.7, Windows 7 (32bit), Chinese Language Pack
'''

import time, re
import bs4 # 必须导入，因为需要做一些bs4专有类型的判断
from bs4 import BeautifulSoup


def test_BeautifulSoup():
	"""
		# BeautifulSoup的一些问题实在让人蛋大。
		# 这里研究下吧。
	"""
	'''
		# 基础部分
		# 关于bs4的解析速度 #################
		# 仔细阅读文档后发现，文档解析器对速度至关重要！
		# 如果没有安装cchardet模块，那么光一个网页就要7秒！！
		# 还不包括获取网页时间。然而试过后，如过山车一般：
		# 安装了cchardet以后7秒变成了一瞬。
		# 然而，用了几天后又变回了7秒，卸载了cchardet又变回了一瞬间！
		# 另外，BeautifulSoup升级到4以后，导入方法变了，如下：
	'''
	from bs4 import BeautifulSoup

	'''
		# 关于被解析文档的编码格式 ##########
		# 又不淡定了，官方说无论被传入什么编码的文档，都会被统一为unicode
		# 实际上有时候我发现，必须以unicode传入才能获得正确结果。。。
		# 这里试验发现，还真的是如此!必须传入decode过的码
	'''
	html_doc = open('page-sm1.html', 'r').read().decode('utf-8')


	'''
		# 关于bs4的文档解析器 ##############
		# 又是一个大坑：bs升级到4后，实例化时需要明确指定文档解析器，如：
		# soup = BeautifulSoup(html_doc, 'lxml')
		# 但是著名的lxml在这里就是个大坑啊，
		# 因为它会直接略过html所有没写规范的tag，而不管人家多在乎那些信息
		# 因为这个解析器的事，我少说也折腾了好几个小时才找到原因吧。
		# 总结：记住，选择html5lib！效率没查多少，最起码容错率强，不会乱删你东西！
	'''
	soup = BeautifulSoup(html_doc, 'html5lib')

	
	'''
		# 关于bs4的输出格式 #################
		# prettify()官方解释是一律输出utf-8格式，
		# 其实却是unicode类型！！所以必须在prettify()里面指定编码。
	'''
	# output = soup.prettify('utf-8')
	# print repr(output)

	'''
		# 所谓的多种搜索节点方式##############
		就是不知道为什么:
		无论怎么测验，find()和find_all()就是死活不管用！
		只有用官方文档里的英文版《爱丽丝》测试才没问题。
		也就是说，问题还是出在了文字编码上？
		可是当我试着查找英文时，搜索结果还是为零-_-!
		到了最后，bs4中众多的搜索工具上，
		唯一能用的就是select()了，即CSS选择器。
		虽然极其好用，但还是有限制性。
		不死心，所以我还是再试验一下find_all()的毛病吧。
	'''
	# == find_all()之搜索标签名称 ============ OK
	# result = soup.find_all('dl') # OK

	# == find_all()之搜索标签属性 ============ not all OK
	# result = soup.find_all(id='newlist_list_div') # OK
	# result = soup.find_all(href=re.compile('.htm')) # Failed 竟然不支持href搜索，和官方说的不一样
	# result = soup.find_all(name='vacancyid') # Failed 不支持标签的name属性搜索

	# == find_all()之按CSS搜索 ============ OK
	# result = soup.find_all('div', class_='clearfix') # OK
	# result = soup.find_all('div', class_=re.compile('newlist_detail')) # OK
	# result = soup.find_all(class_=re.compile('newlist_detail')) # OK

	# == find_all()之按内容text搜索 ============ 
	# find_all()加上text参数后，
	# 返回的是字符串！而不是tag！！
	# 类型为：<class 'bs4.element.NavigableString'>
	# result = soup.find_all(text='会计') # OK 内容必须完全相等才算！（不含子标签） 
	# result = soup.find_all(text=u'数据') # OK 内容必须完全相等 无所谓unicode了
	# result = soup.find_all(text=re.compile(u'学历：')) # OK unicode是绝对要！否则不行！

	# == select() , CSS选择器搜索引擎 ============ 
	'''
		CSS选择器的语法请看w3cschool的文档：
		http://www.w3school.com.cn/cssref/selector_nth-of-type.asp
		下面总结了在BeautifulSoup中的语法搜索：
		标签搜索，如：'input' ,搜索所有标签为input的元素
		宽泛路径，如：'body a' ,就是body内所有a元素
		绝对路径，如：'body > div > div > p' ,必须完全符合路径才能搜到
		ID搜索  ，如：'#tag-1' ,搜索id为tag1的标签
		混合搜索，如：'div #tag1', 搜索id为xx的div标签
			'div[class*=newlist_detail] ~ div[class*=newlist_detail]' ,大混合
		属性存在，如：'a[href]' ,搜索所有存在href属性的a标签
		类名搜索，如：'[class=clearfix]' ,找到class名等于clearfix的标签
			'[class^=newlist_detail]' ,找到class名中以"newlist_detail"开头的标签
			'[class$=zwmc]'           ,找到class名中以"zwmc"结尾的标签
			'[class*=clearfix]'       ,找到class名中包含"zwmc"的标签
		兄弟搜索，如：
			'#links ~ .clearfix' ,找到id为links标签的所有class等于"clearfix"的兄弟标签
			'#links + .clearfix' ,找到id为links标签的下一个class等于"clearfix"的兄弟标签
		序列搜索，如：'p nth-of-type(3)' ,这个说白了就是选择第3个p标签
			'p nth-of-type(odd)' 表示奇数的p标签
			'p nth-of-type(even)' 表示偶数的p标签
			'p nth-of-type(n)' 表示所有的p标签
			'p nth-of-type(3n)' 表示3的倍数的p标签
			'p nth-of-type(4n+1)' 表示4的倍数加1的p标签，如第5个、第9个
	'''
	# result = soup.select('dl > p') # OK tag路径搜索
	# result = soup.select('div[class*=newlist_detail] ~ div') # OK 各种混合搜索
	# result = soup.select('[class*=zwmc]') # OK 各种混合搜索
	con = soup.select('div[class^=newlist_detail]')[0]
	result = con.select('[class*=zwmc]')
	# print type(result[0])

	print len(result) 

	# out = soup.select('[class*=zwmc]')
	# print len(out)
	# for item in out:
	# 	print item.get_text().encode('utf-8')

def bsText(tags=[], info=''):
	if len(tags):
		t = tags[0] # 因为只会有一个对象
		# select()选择器返回的是tag标签
		# 而find_all()用text查询是返回的是字符串！
		if isinstance(t, bs4.element.Tag):
			return t.get_text().encode('utf-8')
		elif isinstance(t, bs4.element.NavigableString):
			return t.string.encode('utf-8')
	else:
		return '无[%s]信息'%info

# 计算时间
def timeup(func):
	start = time.clock()
	func()
	end = time.clock()
	timeuse = end-start
	print '\n[%s()]函数一共使用了%d秒时间。\n' %(func.__name__, timeuse)
	return timeuse

if __name__ == '__main__':
	timeup(test_BeautifulSoup)

