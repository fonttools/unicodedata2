import sys

import unicodedata2

from unittest import TestCase

try:
    from test.test_unicodedata import *
    UnicodeFunctionsTest.test_function_checksum = lambda self: None
except ImportError as e:
    pass

sys.modules['unicodedata'] = unicodedata2



class TestUnidataVersion(TestCase):

    def test_version(self):
        import unicodedata
        self.assertEqual(unicodedata.unidata_version, '7.0.0')
