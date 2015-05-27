# _*_ coding=utf-8 _*_
import sys
import locale
print locale.getpreferredencoding()
#print "测试".encode(locale.getpreferredencoding())

# getting sys.stdout encoding
print sys.stdout.encoding


# using code page CP850,cp1251

#powershell.exe -NoExit /c "chcp.com 65001"