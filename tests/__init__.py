import sys

import unicodedata2

from unittest import TestCase

sys.modules['unicodedata'] = unicodedata2

try:
    from test.test_unicodedata import *
    del test_main
    UnicodeFunctionsTest.expectedchecksum = '61a3f241df846792b34f2b336369e707fa10541e'
except ImportError as e:
    pass




class TestUnidataVersion(TestCase):

    def test_version(self):
        import unicodedata
        self.assertEqual(unicodedata.unidata_version, '7.0.0')
