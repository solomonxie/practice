#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @author mingcheng<i.feelinglucky@gmail.com>
# @site   http://www.gracecode.com/
# @date   2010-01-22

import eyeD3, re, os, sys, time, urllib, urllib2, cookielib, StringIO, gzip
 
#urlread = lambda url: urllib.urlopen(url).read()

class getAlbumCover:
    '''从豆瓣获取专辑封面数据，并写入对应的 mp3 文件'''

    _eyeD3 = None

    # 豆瓣搜索以及专辑封面相关的 API 和格式
    # 2012-12-10: Update by mingcheng - 豆瓣更改地址了，更新脚本
    _doubanSearchApi    = 'http://music.douban.com/subject_search?search_text={0}&cat=1001'
    _doubanCoverPattern = '<img src="http://img3.douban.com/spic/s(\d+).jpg"'
    _doubanConverAddr   = 'http://img3.douban.com/lpic/s{0}.jpg'
    
    artist = '' # 演唱者
    album  = '' # 专辑名称
    title  = '' # 歌曲标题

    def __init__(self, mp3):
        self._eyeD3 = eyeD3.Tag()

        # file exists or readable?
        try:
            self._eyeD3.link(mp3)
            self.getFileInfo()
        except:
            print '读取文件错误'

    def urlread(self, url, need_gzip = True, host = "www.douban.com"):
        req = urllib2.Request(url)
        #req.add_header(header)
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1")
        req.add_header("Referer", "http://music.douban.com/")
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        req.add_header("Accept-Encoding", "gzip, deflate")
        req.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
        req.add_header("Connection", "keep-alive")
        req.add_header("Host", host)
        req.add_header("Cookie", 'bid="9vSv1w9XJNs"; report=ref=%2Fsubject_search&mus_msc=musmsc_1') 

        source = urllib2.urlopen(req).read()

        if need_gzip == True:
            data = StringIO.StringIO(source)
            gzipper = gzip.GzipFile(fileobj=data)
            source = gzipper.read()

        #print source
        return source
        

    def updateCover(self, cover_file):
        '''更新专辑封面至文件'''
        try:
            self._eyeD3.removeImages()
            # cover exists or readable?
            #self._eyeD3.removeLyrics()
            #self._eyeD3.removeComments()
            self._eyeD3.addImage(3, cover_file, u'')
            self._eyeD3.update()
            return True
        except:
            print '修改文件错误'
            return False

    def getFileInfo(self):
        ''' 获取专辑信息 '''
        self.artist = self._eyeD3.getArtist().encode('utf-8')
        self.album  = self._eyeD3.getAlbum().encode('utf-8')
        self.title  = self._eyeD3.getTitle().encode('utf-8')

    def getCoverAddrFromDouban(self, keywords = ''):
        ''' 从豆瓣获取专辑封面的 URL '''
        if not len(keywords):
            keywords = self.artist + ' ' + (self.album or self.title)

        #print keywords
        request = self._doubanSearchApi.format(urllib.quote(keywords))
        result  = self.urlread(request)
        if not len(result):
            return False

        match = re.compile(self._doubanCoverPattern, re.IGNORECASE).search(result)
        if match:
            return self._doubanConverAddr.format(match.groups()[0])
        else:
            return False


if __name__ == "__main__":
    for i in sys.argv:
        if re.search('.mp3$', i):
            print '> 正在处理:', i
            handler = getAlbumCover(i)
            if handler.artist and (handler.album or handler.title):
                print '\t[内容]', handler.artist, handler.title,
                cover_addr = handler.getCoverAddrFromDouban()
                #print cover_addr
                if cover_addr:
                    cover_file = 'cover.jpg'
                    f = file(cover_file, 'w')
                    f.write(handler.urlread(cover_addr, False, "img3.douban.com"))
                    f.close()
                    if handler.updateCover(cover_file):
                        print '[完成]'
                    else:
                        print '[失败]'
                    os.remove(cover_file)
                else:
                    print '[失败]'
            handler = None
            time.sleep(3) # 间隔 3s ，防止被豆瓣 Block

# vim: set et sw=4 ts=4 sts=4 fdm=marker ff=unix fenc=utf8 nobomb ft=python:
