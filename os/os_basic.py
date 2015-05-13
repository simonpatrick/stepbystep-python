# _*_ coding=utf-8 _*_
import os

__author__ = 'patrick'

# return a random bytes suitable for cryptographic use.
print os.urandom(3)
print os.getcwd()
print os.getcwdu()
print os.getegid()
print os.getgid()
print os.getgroups()
#print os.getpgid()
print os.getppid()
#file
try:
    os.mkdir('test',0777)
except OSError:
    print('ignore the file existing error')
os.chdir('test')

with open('test.py',mode='wb'):
    pass
print os.listdir(os.getcwd())

os.rename('test.py','test1.py')
print os.listdir(os.getcwd())
print os.chdir('../')
print os.getcwd()
'''todo how to remove dir in python'''
print os.rmdir('test')
