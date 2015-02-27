# _*_ coding=utf-8 _*_
__author__ = 'patrick'

import pickle

mylist = ["this", "is", 4, 13327]
myfile = open(r"text.txt", "w")
myfile.write("this is sample string")
pickle.dump(mylist, myfile)
myfile.close()

myfile=open(r"text.txt")
loadedlist = pickle.load(myfile)
myfile.close()
print loadedlist

