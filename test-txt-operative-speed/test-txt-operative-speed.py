# coding:utf-8
import time
##################################
"""
# 用read()和来读取1G文件的速度
start = time.clock()
f = open('hello-1g.txt', 'r')
#因为内容太长了，print是看不出处理速度的
#所以直接赋予变量了
content = f.read()
f.close()
end = time.clock()
print str(end-start)
"""

##################################
#"""
# 用readline()和来读取1G文件的速度
start = time.clock()
f = open('hello-1g.txt', 'r')
print f.readline().decode('gb2312')
print f.readline().decode('gb2312')
print f.readline().decode('gb2312')
print f.readline().decode('gb2312')
print f.readline().decode('gb2312')
f.close()
end = time.clock()
print str(end-start) #用了0.08秒
#"""
##################################
"""
start = time.clock()
f = open('hello.txt', 'r') # 原文件14M
f2 = open('hello-1g.txt','a')
content = f.read()
f.close()
# 想要生成1.4G的txt文件
# 用来测试各种方式读写大文件的速度
for i in range(1000):
    f2.write(content)
f2.close()
end = time.clock()
print str(end-start) # 用了446秒
"""
##################################
"""
start = time.clock()
f = open('hello.txt', 'r+')
f2 = open('hello2.txt', 'w')
n = 0
while True:
    line = f.readline()
    n += 1
    if line:
        f2.write(line)
        #print '现在正在写入第 %s 行数据。' % n
    else:
        break
f2.close
f.close()
end = time.clock()
print str(end - start)
"""
##################################
"""
start = time.clock()
f = open('hello.txt', 'r+')
f2 = open('hello2.txt', 'w')
f2.write(f.read())
f2.close
f.close()
end = time.clock()
print str(end - start)
"""
