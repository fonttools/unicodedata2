import sys

import unicodedata2

from unittest import TestCase

sys.modules['unicodedata'] = unicodedata2

try:
    from test.test_unicodedata import *
    del test_main
    UnicodeFunctionsTest.expectedchecksum = '4a0bbb2143360a7b77b1ab424ef013a01d08c75a'
except ImportError as e:
    print 'Could not import python tests'
else:
    if sys.version_info < (2, 7):
        del UnicodeFunctionsTest.test_function_checksum  # The checksums are different on 2.6


class TestUnidataVersion(UnicodeFunctionsTest):

    def test_version(self):
        import unicodedata
        self.assertEqual(unicodedata.unidata_version, '9.0.0')

    def test_east_asian_width_9_0_changes(self):
        self.assertEqual(self.db.ucd_3_2_0.east_asian_width(u'\u231a'), 'N')
        self.assertEqual(self.db.east_asian_width(u'\u231a'), 'W')

del UnicodeFunctionsTest
