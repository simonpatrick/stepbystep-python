# _*_ coding=utf-8 _*_
from inspect import isgeneratorfunction
import types

__author__ = 'patrick'
class Fab(object):
    def __init__(self,max):
        self.max=max
        self.n,self.a,self.b=0,0,1

    def __iter__(self):
        return self

    def next(self):
        if self.n<self.max:
            r=self.b
            self.a,self.b =self.b,self.a+self.b
            self.n=self.n+1
        raise StopIteration()

for f in Fab(5):
    print "print generator"
    print f


def fab(max):
    n,a,b=0,0,1
    while n<max:
        yield b
        a,b=b,a+b
        n=n+1

"""
generator for function
一个带有 yield 的函数就是一个 generator，
它和普通函数不同，生成一个 generator 看起来像函数调用，
但不会执行任何函数代码，
直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。
虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，
并返回一个迭代值，下次执行时从 yield 的下一个语句继续执行。
看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，
每次中断都会通过 yield 返回当前的迭代值。
"""
for n in fab(5):
    print n
    print fab(5).next()

print isgeneratorfunction(fab)
print isinstance(fab,types.GeneratorType)
print isinstance(fab(5),types.GeneratorType)


def read_file(path):
    BLOCK_SIZE=1024
    with open(path,'rb') as f:
        while True:
            block=f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return
