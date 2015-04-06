# _*_ coding=utf-8 _*_
__author__ = 'patrick'

"""
A class that uses different static function depending of a parameter passed in
init. Note the use of a single dictionnary instead of multiple conditions
"""


class Category(object):
    def __init__(self, parm):

        self._static_method_choices = {'param_value_1': self._static_method_1,
                                       'param_value_2': self._static_method_2}
        if parm in self._static_method_choices.keys():
            self.parm = parm
        else:
            raise Exception("invalid parameter {}".format(parm))

    @staticmethod
    def _static_method_1():
        print "static method 1"

    @staticmethod
    def _static_method_2():
        print "static method 2"

    def main_method(self):
        self._static_method_choices[self.parm]()


if __name__ == '__main__':
    category = Category('param_value_1')
    category.main_method()

    category = Category('param_value_2')
    category.main_method()
