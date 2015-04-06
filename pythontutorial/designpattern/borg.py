# _*_ coding=utf-8 _*_
__author__ = 'patrick'

"""
shared state, why all the object share the sane
"""


class Borg(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = "INIT"

    def __str__(self):
        return self.state


class MyBorg(Borg):
    pass


if __name__ == '__main__':
    rm1 = Borg()
    rm2 = Borg()

    rm1.state = "INIT"
    rm2.state = "RUNNING"

    print("RM1:{0}".format(rm1))
    print("RM2: {0}".format(rm2))

    rm2.state = "ZOMBIE"

    print("RM1:{0}".format(rm1))
    print("RM2: {0}".format(rm2))

    print("RM1:{0}".format(id(rm1)))
    print("RM2: {0}".format(id(rm2)))

    rm3= MyBorg()


    print("RM1:{0}".format(rm1))
    print("RM2: {0}".format(rm2))
    print("RM3: {0}".format(rm3))
