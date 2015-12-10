# -*- coding: utf-8 -*-
'''
	# Title : 智联招聘信息爬虫 - 搜索列表部分
	# Author: Solomon Xie
	# Usage : A practise with python: 
				get job information from a chinese job seeking web Zhilian.com.
				This little project is auctually a web crawler, 
				which uses some techniques such as BeautifulSoup and urllib2 and so on.
	# Update: v1.0 已经能够获取
'''
# 必备模块
import urllib2, urllib, re
from bs4 import BeautifulSoup
# 小工具用模块
import time, urlparse
# 如果要做一些bs4专有类型的判断就必须导入
# import bs4 

def ZhilianFetch(keyword='数据', page=1):
	global global_guid , global_total_results, global_current_page

	print '=========== Tring processing Page %d ==========='%page
	baseUrl = 'http://sou.zhaopin.com/jobs/searchresult.ashx'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
	data_filter = {
		'kw' : keyword, # 搜索关键词
		'sm' : '0', # 显示方式代码： 列表是'0',详细是'1'。显示不同源码也不同，尽量选列表模式，源码更好解析。
		'jl' : '北京', # 搜索城市：'北京'，多项用'+'连接(URL编码为%2B)
		#'bj' : '', # 职位类别代码：互联网产品/运营管理 的代码为 '160200'，多项用'%3B'连接(URL编码的%)
		#'in' : '', # 行业代码：多项用';'连接(URL编码为%3B)
		'kt' : '0', # 关键词搜索范围：全文'0' | 公司名'1' | 职位名'2'
		'isadv' : '0', # 是否高级搜索：快速搜索'0' | 高级搜索'1'
		# 'isfilter' : '1', # 是不是筛选器： '0' | '1'
		# 'ispts' : '', # 通常为 '1'
		#'sj' : '', # 职位子类别代码：
		# 'gc' : '5号', # 地铁线路： '5号'
		# 'ga' : '立水桥', # 地名或地铁站名： '天通苑南' 、 '小汤山'
		# 'sb' : '0', # 排序方式代码：默认排序是'0',相关度排序是'1', 首发日排序是'2'
		#'fjt' : '10000', # 职位标签 五险一金'10000' 年底双薪'10001' 绩效奖金'10002' 等等
		# 'sf' : '-1', # 月薪底线：'8001' 不限是'-1'
		# 'st' : '-1', # 月薪上限：'10000' 不限是'-1'
		# 'ct' : '-1', # 公司性质代码
		# 'el' : '-1', # 学历代码
		# 'we' : '-1', # 工作经验代码
		# 'et' : '-1', # 职位类型代码：兼职'1' 全职'2' 实习'4'
		# 'pd' : '-1', # 发布时间(天数)：一周是'7'，一个月是'30'，不限是'-1'
		'p' : page, # 页码，超出总页码时，则会显示最后一页
		#'gr' : '', # 
		# 're' : '2015', # 这个限制了搜素数量，但是其实也不是按年份搜索
		'sg' : global_guid, # 也是叫guid，这是一个随机参数，不知道有什么作用，有可能故意阻挡爬虫可读取的数量
		#'' : '' #
	}

	'''
	# 以上为获取信息之前的准备工作，占用时间极断，且不容易出问题。
	# 下面开始正式解析。遇到编码错误、搜索错误会较多。
	'''
	# === Post方式获取源码 ===
	# req = urllib2.Request(baseUrl, urllib.urlencode(data_filter), headers)
	# src = urllib2.urlopen(req) # 智联招聘屏蔽了Post方式，会给你呈现一堆广告
	# === Get 方式获取源码 ===
	fullUrl = '%s?%s' %(baseUrl, urllib.urlencode(data_filter))
	src = urllib2.urlopen(fullUrl)
	global_current_page += 1 # 更新当前页码
	oriUrl = src.geturl() # 获取真实Url网址
	print 'Processing Url: %s' %fullUrl # 显示正在处理的网页
	# === 本地方式读取源码 ===
	# src = open('test-Zhilian-list-page-sm0.html', 'r') # 测试用，0.001秒
	html_doc = src.read().decode('utf-8') # 用时1秒。


	# === BeautifulSoup解析源码，也是最花时间的，解析器不对则会造成7秒/页面 ===
	soup = BeautifulSoup(html_doc, 'html5lib')

	# === 获取搜索结果的数量 ===
	nums = soup.select('[class$=search_yx_tj] em')
	if len(nums):
		global_total_results = int(nums[0].get_text())
	if global_total_results == 0: return 0 # 如果当前页面没有结果，则不进行处理了。
	print 'There are %d results found as total.' %global_total_results

	# 获取防爬虫的随机码，即url中的sg参数
	tags = soup.select('#guid')
	global_guid = tags[0]['value'] if len(tags)  else ''
	print 'The "guid" is %s.' %global_guid

	# 获取下一页的链接
	tags = soup.select('a[class$=next-page]')
	nextHref = tags[0]['href'] if len(tags) else 0
	# print 'Next page number is %d \n' %nextPage
	return ''

	# 获取真实页码
	# 实际上，智联招聘网页不会自动跳转真实页码，页码是多少都会显示内容
	# 所以这句也就没多大用了
	oriPage = int(urlParam(oriUrl)['p'])
	# print 'The current real page number is %d.' %oriPage

	'''
	# -*- 搜索：CSS选择器方式 soup.slect('') -*-
	# 事实证明，对于巨多不合格网页源码来说，用CSS选择器是最靠谱的了
	# 不过需要稍稍了解下`CSS选择器的语法`。
	'''
	# class$=xx指以xx结尾的class名
	# 因为智联有很多的class名都是以"newlist"开头，
	# 所以只能以它结尾来搜索，否则会匹配到好多不正确的列表。
	records = soup.select('[class$=newlist]')
	print '=== Detected %d Job Information' %len(records)
	output = '' # 储存待输出的内容
	if len(records):
		data = ''
		for row in records:
			data = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' %(
				bsText(row, '[class$=zwmc]', '职位名称') ,     # 职位名称
				bsText(row, '[class$=fk_lv]', '反馈率') ,      # 反馈率
				bsText(row, '[class$=gsmc]', '公司名称') ,     # 公司名称
				bsText(row, ['[class$=zwyx]', {'t':u'职位月薪：'}], '职位月薪') , # 职位月薪
				bsText(row, ['[class$=gxsj]', 'dl p'],              '更新时间'),  # 更新时间
				bsText(row, {'t':u'地点：'}, '工作地点') ,     # 工作地点
				bsText(row, {'t':u'公司性质：'}, '公司性质') , # 公司性质
				bsText(row, {'t':u'公司规模：'}, '公司规模') , # 公司规模
				bsText(row, {'t':u'经验：'}, '工作经验') ,     # 工作经验
				bsText(row, {'t':u'学历：'}, '学历背景') ,     # 学历背景
				bsText(row, {'t':u'岗位职责：'}, '公司规模')   # 公司规模
			)
			# output = data['gzdd'] + '\n' # OK 测试字典格式数据用
			# print data['gzdd'] # OK 测试字典格式数据用
			# 事实证明，这里最好还是用字符串，，因为除了它之外列表、字典之类都没法保证正确的编码输出。
			output += '%s\n%s\n' %(data, '='*40)
			# print data # 测试用
			# break # 测试用：只处理一行数据
			# print 'Got a job info.'
	# 输出结果
	if output:
		f = open('./data/page-log-%d.txt'%oriPage, 'w')
		f.write(output)
		f.close()
	
	print '%sDone of retrieving page %d' %('_'*80, oriPage)
	return oriPage # 返回已经处理的当前页面的“实际”页码

# 读取url中的参数，并以dict字典返回所有参数
def urlParam(url=''):
    query  = urlparse.urlparse(url).query
    params = dict([(key,value[0]) for key, value in urlparse.parse_qs(query).items()])
    return params

# 根据搜索条件，返回搜索结果的字符串
# 如果pattr是str字符串，则用select选择器搜索结果
# 如果pattr是dict 字典，则用find_all()搜索结果
# 如果pattr是list 列表，则分别递归自己直到找出结果
def bsText(tag, pattr, info=''):
	if isinstance(pattr, str): # 如果是str字符串，则用select选择器搜索结果
		result = tag.select(pattr)
		if len(result): return result[0].get_text().encode('utf-8') # 如果结果不是1个那就不正常了
		# else:           print '=== Fail: %s->0' %repr(pattr) # 返回搜索失败信息
	elif isinstance(pattr, dict) and pattr['t']: # 是dict 字典，则用find_all()搜索结果
		result = tag.find_all(text=re.compile(pattr['t']))
		if len(result): return result[0].string.encode('utf-8')
		# else:           print '=== Fail: "%s")->0' %pattr['t'].encode('utf-8') # 返回搜索失败信息
	elif isinstance(pattr, list) and len(pattr): # 如果是list 列表，则分别递归本函数直到找出结果
		for p in pattr:
			result = bsText(tag, p)
			if result : return result
	# 如果前面没有得到返回值，则返回空值
	# return '无[%s]信息'%info # 测试用
	return ''

# 计算时间
def timeup(foo, attr1, attr2):
	start = time.clock()
	val = foo(attr1, attr2)
	end = time.clock()
	timeuse = end-start
	print '=== Spend %d sec. on running %s()\n' %(timeuse, foo.__name__)
	return val

if __name__ == '__main__':
	# === 声明几个公用变量 ===
	global global_guid , global_total_results, global_current_page
	global_guid = '' # 智联招聘用的防爬虫的随机码
	global_total_results = 0 # 搜索结果总数量
	global_current_page  = 1 # 当前处理的页码 
	# timeup(ZhilianFetch, '数据', 1) # 在线解析3秒，本地解析2秒

	# 循环读取每一页的信息
	# 智联招聘一般全网同时会有100,000个职位
	# 但是都不超过90个页面，一页有40个，所以顶多只能获取3600个
	# 另外，如果页码超过现有的，则会仍显示一些招聘信息，但是都是重复的。
	# 唯一不同是，上方会显示“共0个职位满足条件”
	for p in range(1,20): 
		cur = timeup(ZhilianFetch, '数据', p)
		if cur < p : break # 如果页码无效、或已处理过、或失败，就停止处理。
	
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