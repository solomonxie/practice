# -*- coding: utf-8 -*-
'''
	# Title : 智联招聘信息爬虫
	# Author: Solomon Xie
	# Usage : A practise with python: 
				get job information from a chinese job seeking web Zhilian.com.
				This little project is auctually a web crawler, 
				which uses some techniques such as BeautifulSoup and urllib2 and so on.
'''
import urllib2, urllib
import time, re
import bs4 # 必须导入，因为需要做一些bs4专有类型的判断
from bs4 import BeautifulSoup

def ZhilianFetch(keyword = '数据'):
	url = 'http://sou.zhaopin.com/jobs/searchresult.ashx'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
	data_filter = {
		'kw' : keyword, # 搜索关键词
		'sm' : '1', # 显示方式代码： 列表是'0',详细是'1'。显示不同源码也不同，尽量选列表模式，源码更好解析。
		'jl' : '北京', # 搜索城市：'北京'，多项用'+'连接(URL编码为%2B)
		#'bj' : '', # 职位类别代码：互联网产品/运营管理 的代码为 '160200'，多项用'%3B'连接(URL编码的%)
		#'in' : '', # 行业代码：多项用';'连接(URL编码为%3B)
		'kt' : '0', # 关键词搜索范围：全文'0' | 公司名'1' | 职位名'2'
		# 'isadv' : '0', # 是否高级搜索：快速搜索'0' | 高级搜索'1'
		# 'isfilter' : '1', # 是不是筛选器： '0' | '1'
		# 'ispts' : '', # 通常为 '1'
		#'sj' : '', # 职位子类别代码：
		'gc' : '5号', # 地铁线路： '5号'
		'ga' : '立水桥', # 地名或地铁站名： '天通苑南' 、 '小汤山'
		# 'sb' : '0', # 排序方式代码：默认排序是'0',相关度排序是'1', 首发日排序是'2'
		#'fjt' : '10000', # 职位标签 五险一金'10000' 年底双薪'10001' 绩效奖金'10002' 等等
		# 'sf' : '-1', # 月薪底线：'8001' 不限是'-1'
		# 'st' : '-1', # 月薪上限：'10000' 不限是'-1'
		# 'ct' : '-1', # 公司性质代码
		# 'el' : '-1', # 学历代码
		# 'we' : '-1', # 工作经验代码
		# 'et' : '-1', # 职位类型代码：兼职'1' 全职'2' 实习'4'
		# 'pd' : '-1', # 发布时间(天数)：一周是'7'，一个月是'30'，不限是'-1'
		'p' : '1', # 页码，超出总页码时，则会显示最后一页
		#'gr' : '', # 
		're' : '2015', #
		#'' : '' #
	}
	# 这一步的时间几乎可以忽略不计
	req = urllib2.Request(url, urllib.urlencode(data_filter), headers)
	print url+ '?' + urllib.urlencode(data_filter) # 显示正在处理的网页

	'''
	# 以上为获取信息之前的准备工作，占用时间极断，且不容易出问题。
	# 下面开始正式解析。遇到编码错误、搜索错误会较多。
	'''
	# urlopen().read()会占用很长时间，1秒左右
	# 同样的源码，网页解析不出来，存到本地就可以。
	# html_doc = urllib2.urlopen(req).read().decode('utf-8') 
	# 测试时用本地网页,0.001秒
	html_doc = open('test-Zhilian-list-page-sm1.html', 'r').read().decode('utf-8')
	soup = BeautifulSoup(html_doc, 'html5lib')

	'''
	# -*- 搜索：CSS选择器方式 soup.slect('') -*-
	# 事实证明，对于巨多不合格网页源码来说，用CSS选择器是最靠谱的了
	# 不过需要稍稍了解下`CSS选择器的语法`。
	'''
	####### 以下匹配引擎，只适合智联招聘的“详细”页面，url中sm参数需设置为1。
	# 找到'大容器'，再对它进行操作
	results = soup.select('div#newlist_list_content_table')
	output  = '' # 储存输出结果
	if len(results):
		container = results[0] # 一个页面只能有一个'大容器'
		# 开始对'大容器'中的多条记录进行拆分
		# class$=xx指以xx结尾的class名
		# 因为智联有很多的class名都是以"newlist"开头，
		# 所以只能以它结尾来搜索，否则会匹配到好多不正确的列表。
		records = container.select('div[class$=newlist]')
		print len(records)
		if len(records):
			data = ''
			for row in records:
				data = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' %(
					bsText(row.select('[class*=zwmc]'), '职位名称') , # 职位名称
					bsText(row.select('[class*=fk_lv]'), '反馈率') , # 反馈率
					bsText(row.select('[class*=gsmc]'), '公司名称') , # 公司名称
					bsText(row.select('[class*=zwyx]'), '职位月薪') , # 职位月薪
					bsText(row.find_all(text=re.compile(u'地点：')), '工作地点') , # 工作地点
					bsText(row.find_all(text=re.compile(u'公司性质：')), '公司性质') , # 公司性质
					bsText(row.find_all(text=re.compile(u'公司规模：')), '公司规模') , # 公司规模
					bsText(row.find_all(text=re.compile(u'经验：')), '工作经验') , # 工作经验
					bsText(row.find_all(text=re.compile(u'学历：')), '学历背景') , # 学历背景
					bsText(row.find_all(text=re.compile(u'岗位职责：')), '公司规模') , # 公司规模
					bsText(row.select('dl p'), '更新时间') # 更新时间
				)
				# output = data['gzdd'] + '\n' # OK 测试字典格式数据用
				# print data['gzdd'] # OK 测试字典格式数据用
				# 事实证明，这里最好还是用字符串，，因为除了它之外列表、字典之类都没法保证正确的编码输出。
				output += '%s\n%s%s' %(data, '='*40, '\n\n')
				# ls = row.select('[class*=zwmc]')
				# print row.prettify('utf-8')
				print data
				# break # 测试用：只处理一行数据
	# 输出结果
	if output:
		f = open('log.txt', 'w')
		f.write(output)
		f.close()

def bsText(tags, info=''):
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
	timeup(ZhilianFetch) # 在线解析3秒，本地解析2秒
	
	'''
	# url编码转换的把戏
	url_ori = 'http://sou.zhaopin.com/jobs/searchresult.ashx?sm=1&jl=数据&p=1&gc=5号&ga=立水桥&kt=0&kw=数据'
	url_coded = '%2fjobs%2fsearchresult.ashx%3fsm%3d1%26jl%3d%25E5%258C%2597%25E4%25BA%25AC%26kt%3d0%26kw%3d%25E6%2595%25B0%25E6%258D%25AE%26gr%3d2%26isfilter%3d1%26p%3d1%26re%3d2015%26ga%3d%25e7%258e%258b%25e8%25be%259b%25e5%25ba%2584'
	print url_ori
	print url_coded
	# 把带中文的ur转换编码成这样的：http%3A//sou.zhaopin.com/jobs/searchresult.ashx%3Fsm%3D1%26jl%3D%E6%95%B0%E6%8D%AE%26p%3D1%26gc%3D5%E5%8F%B7%26ga%3D%E7%AB%8B%E6%B0%B4%E6%A1%A5%26kt%3D0%26kw%3D%E6%95%B0%E6%8D%AE
	print urllib.quote(url_ori)
	# 把正常的url再进一步转换：
	print urllib.quote(urllib.quote(url_ori))
	# 把url解码还原成有正常的url：http://sou.zhaopin.com/jobs/searchresult.ashx?sm=1&jl=%E5%8C%97%E4%BA%AC&kt=0&kw=%E6%95%B0%E6%8D%AE&gr=2&isfilter=1&p=1&re=2015&ga=%e7%8e%8b%e8%be%9b%e5%ba%84
	print urllib.unquote(url_coded)
	# 把正常的url还原成显示中文的url：http://sou.zhaopin.com/jobs/searchresult.ashx?sm=1&jl=北京&kt=0&kw=数据&gr=2&isfilter=1&p=1&re=2015&ga=王辛庄
	print urllib.unquote(urllib.unquote(url_coded))
	'''