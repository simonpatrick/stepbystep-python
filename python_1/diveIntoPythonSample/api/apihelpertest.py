__author__ = 'simon'

import unittest
import apihelper
import sys
from StringIO import StringIO


class Redirector(unittest.TestCase):
    def setUp(self):
        self.savestdout = sys.stdout
        self.redirect = StringIO()
        sys.stdout = self.redirect

    def tearDown(self):
        sys.stdout = self.savestdout


class KnownValues(Redirector):
    def testApiHelper(self):
        apihelper.info(apihelper)
        self.redirect.seek(0)
        self.assertEqual(self.redirect.read(), """info       Print methods and doc strings. Takes module, class, list, dictionary, or string.
""")

class ParamChecks(Redirector):
    def testSpacing(self):
        """info should honor spacing argument"""
        apihelper.info(apihelper, spacing=20)
        self.redirect.seek(0)
        self.assertEqual(self.redirect.read(),
"""info                 Print methods and doc strings. Takes module, class, list, dictionary, or string.
""")

    def testCollapse(self):
        """info should honor collapse argument"""
        apihelper.info(apihelper, collapse=0)
        self.redirect.seek(0)
        self.assertEqual(self.redirect.read(),
"""info       Print methods and doc strings.

	Takes module, class, list, dictionary, or string.
""")

class BadInput(unittest.TestCase):
    def testNoObject(self):
        """info should fail with no object"""
        self.assertRaises(TypeError, apihelper.info, spacing=20)

if __name__ == "__main__":
    unittest.main()