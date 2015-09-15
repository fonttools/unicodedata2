import sys

import unicodedata2

from unittest import TestCase

sys.modules['unicodedata'] = unicodedata2

try:
    from test.test_unicodedata import *
    del test_main
    UnicodeFunctionsTest.expectedchecksum = '97c2dafb4c8258847339c8def763c3618d242c87'
except ImportError as e:
    print 'Could not import python tests'
else:
    if sys.version_info < (2, 7):
        del UnicodeFunctionsTest.test_function_checksum  # The checksums are different on 2.6


class TestUnidataVersion(TestCase):

    def test_version(self):
        import unicodedata
        self.assertEqual(unicodedata.unidata_version, '8.0.0')
