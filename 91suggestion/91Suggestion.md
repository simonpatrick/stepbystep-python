# Python 91 Suggestion
## 1. Pythonic
- The zone of python
- 美
- 简单办法，唯一的简单办法
- 容易解释的实现
- 灵活应用迭代器
```python
    for i in array:
        print i
```
- 安全关闭文件
```python 
with open(file,'r') as f :
    do_something(f)
```
- slice 和python 内置函数
```python
a=[1,2,3,4]
c='abcdert'
print a[::-1]
print c[::-1]
print list(reversed(a))
print list(reversed(c))
```
- 标准库
格式化字符串
```python
    value ={‘greet’:'hello','who':'world'}
    print '%(greet)s %(who)s' % value
```
- 包、模块小写，包通常只在__init__文件里面

