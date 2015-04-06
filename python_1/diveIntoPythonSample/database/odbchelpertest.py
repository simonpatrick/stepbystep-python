__author__ = 'simon'

import unittest
import odbchelper

class GoodInput(unittest.TestCase):
    def testBlank(self):
        self.assertEqual("",odbchelper.buildConnectionString({}))

    def testKnownValue(self):
        params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}
        knownItems = params.items()
        knownItems.sort()
        print knownItems
        knownString = repr(knownItems)
        print knownString
        result = odbchelper.buildConnectionString(params)
        resultItems = [tuple(e.split("=")) for e in result.split(";")]
        resultItems.sort()
        resultString = repr(resultItems)
        self.assertEqual(knownString, resultString)

class BadInput(unittest.TestCase):
    def testString(self):
        # buildConnectionString() and buildConnectionString()
        self.assertRaises(AttributeError,odbchelper.buildConnectionString,"")
    def testList(self):
        self.assertRaises(AttributeError,odbchelper.buildConnectionString,[])
    def testTuple(self):
        self.assertRaises(AttributeError,odbchelper.buildConnectionString,())

if __name__ == '__main__':
    unittest.main()