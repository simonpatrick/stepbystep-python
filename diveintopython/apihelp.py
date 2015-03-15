# _*_ coding=utf-8 _*_
__author__ = 'patrick'


def info(object, spacing=10, collapse=1):
    """print methods and doc string"""
    methodList = [e for e in dir(object) if callable(getattr(object, e))]
    processFunc = collapse and (lambda s: "".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" % (method.ljust(spacing), processFunc(
        str(getattr(object, method).__doc__))) for method in methodList])


if __name__ == "__main__":
    print help.__doc__