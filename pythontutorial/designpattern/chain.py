# _*_ coding=utf-8 _*_
__author__ = 'patrick'

"""http://www.testingperspective.com/wiki/doku.php/collaboration/chetan
/designpatternsinpython/chain-of-responsibilitypattern
"""


class Handler:
    def __init__(self, successor):
        self.successor = successor

    def handler(self, request):
        i = self._handler(request)
        if not i:
            if hasattr(self.successor, "handler"):
                self.successor.handler(request)
            else:
                print "this is end as there is request can be processed"

    def _handler(self, request):
        raise NotImplementedError("must be implemented in subclass")


"""
Concrete Handler
"""


class Handler1(Handler):
    def _handler(self, request):
        print "goes to handler1 "
        if 0 < request <= 10:
            print "handler1 handle {}".format(request)
            return True


class Handler2(Handler):
    def _handler(self, request):
        print "goes to handler2"
        if 10 < request <= 20:
            print "handler2 handler {}".format(request)
            return True


class Handler3(Handler):
    def _handler(self, request):
        print "goes to handler3"
        if 20 < request <= 100:
            print "handler3 handler {}".format(request)
            return True


class DefaultHandler(Handler):
    def _handler(self, request):
        print "goes to default handler"
        if 100 < request <= 1000:
            print "default handler handler {}".format(request)
            return True
        else:
            print "can't handler the request"
            return False


class Client():
    def __init__(self):
        self.handler = Handler1(Handler3(Handler2(DefaultHandler(None))))

    def delegate(self, requests):
        for request in requests:
            self.handler.handler(request)


if __name__ == '__main__':
    requests = [2, 3, 4, 5, 10000, 10, 89, 50, 100]
    client = Client()
    client.delegate(requests)