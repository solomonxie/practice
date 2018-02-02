# coding:utf-8
from multiprocessing import Pool
from multiprocessing.dummy import Pool as Treads
import time
def hello(name):
    sum = 0
    for i in range(20000000): # 经测试 只有最少百万级数字的运算才会真正产生多进程优势
        sum += i
    print('%s:%d'%(name,sum))
    sum = ''

if __name__ == '__main__':
    names=['a','b','c', 'd']
    start = time.time()
    for i in names:
        hello(i)
    end = time.time()
    print 'Single process spend %d seconds.'%(end-start)
    start = time.time()
    np = 2
    pool = Pool(processes=np)
    pool.map(hello,names)
    pool.close()
    pool.join()
    end = time.time()
    print '%d processes spend %d seconds.'%(np, end-start)
    start = time.time()
    np = 4
    pool = Pool(processes=np)
    pool.map(hello,names)
    pool.close()
    pool.join()
    end = time.time()
    print '%d processes spend %d seconds.'%(np, end-start)
    start = time.time()
    np = 2
    pool = Treads(processes=np)
    pool.map(hello,names)
    pool.close()
    pool.join()
    end = time.time()
    print '%d treads spend %d seconds.'%(np, end-start)
    start = time.time()
    np = 4
    pool = Treads(processes=np)
    pool.map(hello,names)
    pool.close()
    pool.join()
    end = time.time()
    print '%d treads spend %d seconds.'%(np, end-start)


'''
测试结果1：
单个进程===》
a:49999995000000
b:49999995000000
c:49999995000000
d:49999995000000
Single process spend 7 seconds.

2个进程===》
a:49999995000000
c:49999995000000
b:49999995000000
d:49999995000000
2 processes spend 5 seconds.

4个进程===》
a:49999995000000
c:49999995000000
b:49999995000000
d:49999995000000
4 processes spend 6 seconds.

2个线程===》
b:49999995000000
a:49999995000000
c:49999995000000
d:49999995000000
2 treads spend 11 seconds.

4个线程===》
a:49999995000000
c:49999995000000
b:49999995000000
d:49999995000000
4 treads spend 11 seconds.




测试结果2：
单个进程===》
a:199999990000000
b:199999990000000
c:199999990000000
d:199999990000000
Single process spend 16 seconds.

2个进程===》
a:199999990000000
c:199999990000000
b:199999990000000
d:199999990000000
2 processes spend 10 seconds.

4个进程===》
a:199999990000000
c:199999990000000
b:199999990000000
d:199999990000000
4 processes spend 13 seconds.

2个线程===》
b:199999990000000
a:199999990000000
c:199999990000000
d:199999990000000
2 treads spend 24 seconds.

4个线程===》
a:199999990000000
c:199999990000000b:199999990000000

d:199999990000000
4 treads spend 23 seconds.


'''