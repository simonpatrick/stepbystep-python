# _*_ coding=utf-8 _*_
__author__ = 'patrick'


class Person(object):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def do_action(self):
        print (self.name, self.action.name)
        return self.action


class Action(object):
    def __init__(self, name):
        self.name = name

    def action(self):
        print(self.name)
        return self

    def stop(self):
        print("then stop")
        return self


if __name__ == '__main__':
    move = Action("move")
    person = Person("patrick", move)
    person.do_action().action().stop().action().stop()
