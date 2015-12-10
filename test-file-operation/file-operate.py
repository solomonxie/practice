# -*- coding: utf-8 -*-

'''
其实就是想把好多年前积累的恩多个txt文件合并到一个里面
没有时间印，没有逻辑没有顺序，所以也不智能处理了。
就简单把他们都合并到一个txt文件里吧，然后再手工粘贴到word里面。
其他的以后再处理 都好说了。。。
主要可以练习的，可能就是基本的文件目录操作吧。
'''

def combineText(path='/text'):
        import os
        # path = (os.getcwdu + u'\\text').encode('gbk')
        unipath = os.getcwdu() + u'\\text'
        files = os.listdir(unipath) # listdir()在接收unicode参数时会返回unicode格式的文件目录
        print '%d files exist.' % len(files)
        print files
        '''
        # 上面实验证明，listdir()返回的unicode格式文件名，是完全正确、可以对应的上原中文的。
        # 利用这个，解码问题解决了。那剩下就是encode编码还原到正确的中文的问题上了。
        # 到这里为止，还是正确的。
        '''
        ###################################################
        for i in range(len(files)) :
            # 这里用utf-8会出错，因为它不会翻译成中文，而只翻译到utf-8格式码
            item = files[i]
            name = item.encode('gbk')
            
            # 如果是目录而不是文件，则跳过
            if os.path.isdir('./text/'+name) : continue 

            # 注意，如果不是utf-8，IDLE命令行是显示不出正确格式的。所以这里稍稍处理了下。
            print '=====正在处理%d文件是【%s】【%s】======' %(i,item.encode('utf-8') ,repr(item))
            
            ###########################################
            '''
            # print repr(name)
            # 上面这一句证明了，这种时候永远不要相信print！所以必须用repr()查看真实值！
            # 同时还证明了，原本正确的unicode格式的name，在还原成gbk时出错了！
            # 例如'你好'，解码到unicode后是'\u4f60\u597d'，这一步没错。
            # 在print时，如果把它encode重新编码到utf-8，就会打印出正确的文件名。
            # 如果用的是gbk编码，那么在IDLE里面显示正常，而在Sublime显示不正常。
            '''
            ##########################################
            with open('total.txt', 'a') as f_new:
                with open('./text/' + name, 'r') as f_old:
                    # print f.read().decode('gbk').encode('utf-8')
                    load = f_old.read()
                    try:
                        content = load.decode('gbk').encode('gbk')
                    except:
                        content = load
                    finally:
                        #print content
                        f_new.write('# FILENAME:%s\n## CONTENT:\n%s\n## END OF CONTENT\n\n' %(item.encode('gbk'), content))
                    f_old.close()
                f_new.close()
                print 'OK'
            '''
            # 直到读取这里，其实还一点问题都没有。
            # 不过经测试，以上文件读取只适用于ANSI格式txt，其他格式保存的txt都会错。
            # 不过限制得这么死，当然了。。。-_-!
            # 懒得想办法根据文件的编码格式再判断了，手动吧。。。
            '''

        ####################################################
        '''
        # 下面这一段却没有问题 正确运行 为什么？
        # 为什么把文件名直接写出来，会和从os.walk中取出来的不一样呢？
        # 那有可能是os.walk()函数出问题了。
        # 然而发现，其实os.listdir()函数也一样
        # 那么，问题就只有`对文件名的解码decode()`出错了。
        # 也就是说，找不到文件名使用的真正编码，就无法通过。
        name = './text/你好.txt'.decode('utf-8').encode('gbk')
        # 这里用utf-8是因为首行已经声明了所有本源码中出现的中文都会变成utf-8
        f = open(name, 'r')
        # print f.read().decode('gbk')
        f.close()
        '''

def renameFiles():
    import os
    unipath = os.getcwdu() + u'\\text'
    files = os.listdir(unipath) # listdir()在接收unicode参数时会返回unicode格式的文件目录
    print '%d files exist.' % len(files)
    print files
    for i in range(len(files)) :
        item = files[i]
        name = item.encode('gbk')
        
        # 如果是目录而不是文件，则跳过
        if os.path.isdir('./text/'+name) : continue 

        # 注意，如果不是utf-8，IDLE命令行是显示不出正确格式的。所以这里稍稍处理了下。
        print '=====正在处理%d文件是【%s】【%s】======' %(i,item.encode('utf-8') ,repr(item))
        os.rename('./text/%s' %name, './text/%s.txt' %str(i))
        print 'OK'

if __name__ == '__main__':
    # combineText()
    renameFiles()
