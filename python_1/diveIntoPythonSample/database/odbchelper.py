__author__ = 'simon'

def buildConnectionString(params):
    return ";".join(["%s=%s" % (k,v) for k,v in params.items()])

if __name__=="__main__":
    myParams ={"server":"test",
               "database":"test",
                "uid":"sa",
                "pwd":"password"}
    print buildConnectionString(myParams)