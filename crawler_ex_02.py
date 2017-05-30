# -*- coding: utf-8 -*-
# 这是用来做黑板课的一个爬虫挑战题，第三关
# http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/
# 注册了一个账号：分别填test123, test123@test123.com, 123123
# 登录后可以正常闯关了
# http://www.heibanke.com/lesson/crawler_ex02/

import urllib, urllib2
import cookielib

def ReadNum(num=0):
    url = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/'

    # 制作cookie
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    # 制作Post表单提交
    data = urllib.urlencode({
        'username' : 'test123',
        'password' : str(num)
    })
    req = urllib2.Request(url, data)
    page = urllib2.urlopen(req)
    print page.read()

if __name__ == '__main__' :
    ReadNum()
