# _*_ coding=utf-8 _*_
import unittest
__author__ = 'patrick'


class MyTests(unittest.TestCase):
    def test_average(self):
        print("my Tests")
        pass

class MyTest2(unittest.TestCase):
    def test_another_test(self):
        print("My Test2")
        pass

def test_suite():
    def _suite(test_class):
        return unittest.makeSuite(test_class)

    suite=unittest.TestSuite()
    suite.addTest((_suite(MyTests),_suite(MyTest2)))
    return suite

unittest.main(defaultTest='test_suite')

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

'''
def setup():
    pass

def teardown():
    pass

'''