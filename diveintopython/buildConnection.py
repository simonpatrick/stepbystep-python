# _*_ coding=utf-8 _*_
__author__ = 'patrick'


def buildConnectionString(params):
    """build connection string from a dic"""
    print params
    print params["key"]
    print params["k1"]
    return " ".join("%s=%s" % (k, v) for k, v in params.items())


params = {"key": "value", "k1": "v1"}
buildConnectionString(params)