#!/bin/sh

echo "start of script."

## Reading method
# read Response
# echo $Response
# echo ${Response} # same with above
# echo $response # case sensitive test

# Standard loop
# for v1 v2 v3 v4  do
#	#statements
# done

# loop file
# for fn in `ls ./`; do # note: it's `, not a '
#     echo $fn
# done

# loop and variable
# for skill in Ada Coffe Action Java; do
#     echo "I am good at ${skill}Script"
# done

# 拼接字符串
# your_name="qinjx"
# greeting="hello, "$your_name" !"
# greeting_1="hello, ${your_name} !"
# echo $greeting $greeting_1 " same result

# 获取字符串长度
# string="abcd"
# echo ${#string} #输出 4

# 提取子字符串
# string="runoob is a great site"
# echo ${string:0:4} # 输出 runo

# 数组操作
# arr1=(96 97 98 99)
# # arr1 = (1 2 3 4) # syntax error: no space around =
# echo ${arr1[3]} # get the 4th element in list
# echo ${arr1[@]} # get all elements in list
# echo ${#arr1[@]} # get length of list
# echo ${#arr1[0]} # get length of an element
# 

# if judge
# x=100; y=100
# if test $[x] -eq $[y]
# then
#     echo '两个数相等！'
# else
#     echo '两个数不相等！'
# fi

# 基本运算
# a=5; b=6
# result=$[a+b]
# echo "result: $result"


# 函数
# demoFun(){
#     echo "这是我的第一个 shell 函数!"
# }
# echo "-----函数开始执行-----"
# demoFun
# echo "-----函数执行完毕-----"

# Parameters for  function
# funWithParam(){
#     echo "第一个参数为 $1 ."
#     echo "第二个参数为 $2 ."
#     echo "第十个参数为 $10 ." # wrong refrerence
#     echo "第十个参数为 ${10} ."
#     echo "第十一个参数为 ${11} ."
#     echo "参数总数有 $# 个."
#     echo "作为一个字符串输出所有参数 $*."
# }
# funWithParam 9 8 7 6 5 4 3 2 1 34 73
# 
