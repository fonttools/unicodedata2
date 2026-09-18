""" Test script for the unicodedata module.

    Written by Marc-Andre Lemburg (mal@lemburg.com).

    (c) Copyright CNRI, All Rights Reserved. NO WARRANTY.

"""

from functools import partial
from pathlib import Path
import sys
import unittest
import hashlib
# from test.support import script_helper

encoding = 'utf-8'
errors = 'surrogatepass'

# Selected tests adapted from CPython 9ab004d41e:
# Lib/test/test_unicodedata.py and Lib/test/test_ucn.py.
# Property tests cover the current database; normalization tests also cover 3.2.0.

### Run tests

# NOTE: UnicodeMethodsTest upstream tests methods on `str` objects, and
# is excluded from the unicodedata2 suite
class UnicodeDatabaseTest(unittest.TestCase):

    def setUp(self):
        # In case unicodedata is not available, this will raise an ImportError,
        # but the other test cases will still be run
        import unicodedata2
        self.db = unicodedata2

    def tearDown(self):
        del self.db

class UnicodeFunctionsTest(UnicodeDatabaseTest):

    # Update this if the database changes. Make sure to do a full rebuild
    # (e.g. 'make distclean && make') to get the correct checksum.
    expectedchecksum = 'f2f46908e4a8ea1616baf2390f5383c12f610c5f'

    def test_function_checksum(self):
        import unicodedata2

        data = []
        h = hashlib.sha1()

        for i in range(sys.maxunicode + 1):
            char = chr(i)
            data = [
                # Properties
                format(self.db.digit(char, -1), '.12g'),
                format(self.db.numeric(char, -1), '.12g'),
                format(self.db.decimal(char, -1), '.12g'),
                self.db.category(char),
                self.db.bidirectional(char),
                self.db.decomposition(char),
                str(self.db.mirrored(char)),
                str(self.db.combining(char)),
                unicodedata2.east_asian_width(char),
                self.db.name(char, ""),
            ]
            h.update(''.join(data).encode("ascii"))
        result = h.hexdigest()
        self.assertEqual(result, self.expectedchecksum)

    def test_aliases(self):
        # Check that the aliases defined in the NameAliases.txt file work.
        # This should be updated when new aliases are added or the file
        # should be downloaded and parsed instead.  See #12753.
        aliases = [
            ('LATIN CAPITAL LETTER GHA', 0x01A2),
            ('LATIN SMALL LETTER GHA', 0x01A3),
            ('KANNADA LETTER LLLA', 0x0CDE),
            ('LAO LETTER FO FON', 0x0E9D),
            ('LAO LETTER FO FAY', 0x0E9F),
            ('LAO LETTER RO', 0x0EA3),
            ('LAO LETTER LO', 0x0EA5),
            ('TIBETAN MARK BKA- SHOG GI MGO RGYAN', 0x0FD0),
            ('YI SYLLABLE ITERATION MARK', 0xA015),
            ('PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRACKET', 0xFE18),
            ('BYZANTINE MUSICAL SYMBOL FTHORA SKLIRON CHROMA VASIS', 0x1D0C5)
        ]
        for alias, codepoint in aliases:
            self.assertEqual(self.db.lookup(alias), chr(codepoint))
            name = self.db.name(chr(codepoint))
            self.assertNotEqual(name, alias)
            self.assertEqual(self.db.lookup(alias),
                             self.db.lookup(name))
            with self.assertRaises(KeyError):
                self.db.ucd_3_2_0.lookup(alias)

    def test_named_sequences_sample(self):
        # Check a few named sequences.  See #12753.
        sequences = [
            ('LATIN SMALL LETTER R WITH TILDE', '\u0072\u0303'),
            ('TAMIL SYLLABLE SAI', '\u0BB8\u0BC8'),
            ('TAMIL SYLLABLE MOO', '\u0BAE\u0BCB'),
            ('TAMIL SYLLABLE NNOO', '\u0BA3\u0BCB'),
            ('TAMIL CONSONANT KSS', '\u0B95\u0BCD\u0BB7\u0BCD'),
        ]
        for seqname, codepoints in sequences:
            self.assertEqual(self.db.lookup(seqname), codepoints)
            with self.assertRaises(KeyError):
                self.db.ucd_3_2_0.lookup(seqname)

    def test_errors(self):
        self.assertRaises(TypeError, self.db.name)
        self.assertRaises(TypeError, self.db.name, 'xx')
        self.assertRaises(TypeError, self.db.lookup)
        self.assertRaises(KeyError, self.db.lookup, 'unknown')

    def test_name_inverse_lookup(self):
        for i in range(sys.maxunicode + 1):
            char = chr(i)
            looked_name = self.db.name(char, None)
            if looked_name:
                self.assertEqual(self.db.lookup(looked_name), char)

    def test_digit(self):
        self.assertEqual(self.db.digit('A', None), None)
        self.assertEqual(self.db.digit('9'), 9)
        self.assertEqual(self.db.digit('\u215b', None), None)
        self.assertEqual(self.db.digit('\u2468'), 9)
        self.assertEqual(self.db.digit('\U00020000', None), None)
        self.assertEqual(self.db.digit('\U0001D7FD'), 7)

        # New in 13.0.0
        self.assertEqual(self.db.digit('\U0001fbf9', None), 9)
        # New in 14.0.0
        self.assertEqual(self.db.digit('\U00016ac9', None), 9)
        # New in 15.0.0
        self.assertEqual(self.db.digit('\U0001e4f9', None), 9)

        self.assertRaises(TypeError, self.db.digit)
        self.assertRaises(TypeError, self.db.digit, 'xx')
        self.assertRaises(ValueError, self.db.digit, 'x')

    def test_numeric(self):
        self.assertEqual(self.db.numeric('A',None), None)
        self.assertEqual(self.db.numeric('9'), 9)
        self.assertEqual(self.db.numeric('\u215b'), 0.125)
        self.assertEqual(self.db.numeric('\u2468'), 9.0)
        self.assertEqual(self.db.numeric('\U00020000', None), None)

        # New in 4.1.0
        self.assertEqual(self.db.numeric('\U0001012A', None), 9000)
        # Changed in 4.1.0
        self.assertEqual(self.db.numeric('\u5793', None), None)
        self.assertEqual(self.db.ucd_3_2_0.numeric('\u5793', None), 1e20)
        # New in 5.0.0
        self.assertEqual(self.db.numeric('\u07c0', None), 0.0)
        # New in 5.1.0
        self.assertEqual(self.db.numeric('\ua627', None), 7.0)
        # Changed in 5.2.0
        self.assertEqual(self.db.numeric('\u09f6'), 3/16)
        self.assertEqual(self.db.ucd_3_2_0.numeric('\u09f6'), 3.0)
        # New in 6.0.0
        self.assertEqual(self.db.numeric('\u0b72', None), 0.25)
        # New in 12.0.0
        self.assertEqual(self.db.numeric('\U0001ed3c', None), 0.5)
        # New in 13.0.0
        self.assertEqual(self.db.numeric('\U0001fbf9', None), 9)
        # New in 14.0.0
        self.assertEqual(self.db.numeric('\U00016ac9', None), 9)
        # New in 15.0.0
        self.assertEqual(self.db.numeric('\U0001e4f9', None), 9)

        self.assertRaises(TypeError, self.db.numeric)
        self.assertRaises(TypeError, self.db.numeric, 'xx')
        self.assertRaises(ValueError, self.db.numeric, 'x')

    def test_decimal(self):
        self.assertEqual(self.db.decimal('A',None), None)
        self.assertEqual(self.db.decimal('9'), 9)
        self.assertEqual(self.db.decimal('\u215b', None), None)
        self.assertEqual(self.db.decimal('\u2468', None), None)
        self.assertEqual(self.db.decimal('\U00020000', None), None)
        self.assertEqual(self.db.decimal('\U0001D7FD'), 7)

        # New in 4.1.0
        self.assertEqual(self.db.decimal('\xb2', None), None)
        self.assertEqual(self.db.decimal('\u1369', None), None)
        # New in 5.0.0
        self.assertEqual(self.db.decimal('\u07c0', None), 0)
        # New in 13.0.0
        self.assertEqual(self.db.decimal('\U0001fbf9', None), 9)
        # New in 14.0.0
        self.assertEqual(self.db.decimal('\U00016ac9', None), 9)
        # New in 15.0.0
        self.assertEqual(self.db.decimal('\U0001e4f9', None), 9)

        self.assertRaises(TypeError, self.db.decimal)
        self.assertRaises(TypeError, self.db.decimal, 'xx')
        self.assertRaises(ValueError, self.db.decimal, 'x')

    def test_category(self):
        self.assertEqual(self.db.category('\uFFFE'), 'Cn')
        self.assertEqual(self.db.category('a'), 'Ll')
        self.assertEqual(self.db.category('A'), 'Lu')
        self.assertEqual(self.db.category('\U00020000'), 'Lo')

        # New in 4.1.0
        self.assertEqual(self.db.category('\U0001012A'), 'No')
        self.assertEqual(self.db.category('\U000e01ef'), 'Mn')
        # New in 5.1.0
        self.assertEqual(self.db.category('\u0374'), 'Lm')
        # Changed in 13.0.0
        self.assertEqual(self.db.category('\u0b55'), 'Mn')
        self.assertEqual(self.db.category('\U0003134a'), 'Lo')
        # Changed in 14.0.0
        self.assertEqual(self.db.category('\u061d'), 'Po')
        self.assertEqual(self.db.category('\U0002b738'), 'Lo')
        # Changed in 15.0.0
        self.assertEqual(self.db.category('\u0cf3'), 'Mc')
        self.assertEqual(self.db.category('\U000323af'), 'Lo')

        self.assertRaises(TypeError, self.db.category)
        self.assertRaises(TypeError, self.db.category, 'xx')

    def test_bidirectional(self):
        self.assertEqual(self.db.bidirectional('\uFFFE'), '')
        self.assertEqual(self.db.bidirectional(' '), 'WS')
        self.assertEqual(self.db.bidirectional('A'), 'L')
        self.assertEqual(self.db.bidirectional('\U00020000'), 'L')

        self.assertRaises(TypeError, self.db.bidirectional)
        self.assertRaises(TypeError, self.db.bidirectional, 'xx')

    def test_decomposition(self):
        self.assertEqual(self.db.decomposition('\uFFFE'),'')
        self.assertEqual(self.db.decomposition('\u00bc'), '<fraction> 0031 2044 0034')

        # Hangul characters (CPython gh-88091), in both database views.
        self.assertEqual(self.db.decomposition('\uAC00'), '1100 1161')
        self.assertEqual(self.db.decomposition('\uD4DB'), '1111 1171 11B6')
        self.assertEqual(self.db.decomposition('\uC2F8'), '110A 1161')
        self.assertEqual(self.db.decomposition('\uD7A3'), '1112 1175 11C2')
        self.assertEqual(self.db.ucd_3_2_0.decomposition('\uAC00'),
                         '1100 1161')
        self.assertEqual(self.db.ucd_3_2_0.decomposition('\uD4DB'),
                         '1111 1171 11B6')
        self.assertEqual(self.db.ucd_3_2_0.decomposition('\uC2F8'),
                         '110A 1161')
        self.assertEqual(self.db.ucd_3_2_0.decomposition('\uD7A3'),
                         '1112 1175 11C2')

        self.assertRaises(TypeError, self.db.decomposition)
        self.assertRaises(TypeError, self.db.decomposition, 'xx')

    def test_mirrored(self):
        self.assertEqual(self.db.mirrored('\uFFFE'), 0)
        self.assertEqual(self.db.mirrored('a'), 0)
        self.assertEqual(self.db.mirrored('\u2201'), 1)
        self.assertEqual(self.db.mirrored('\U00020000'), 0)

        # New in 5.0.0
        self.assertEqual(self.db.mirrored('\u0f3a'), 1)
        self.assertEqual(self.db.mirrored('\U0001d7c3'), 1)
        # New in 11.0.0
        self.assertEqual(self.db.mirrored('\u29a1'), 0)
        # New in 14.0.0
        self.assertEqual(self.db.mirrored('\u2e5c'), 1)
        # New in 16.0.0
        self.assertEqual(self.db.mirrored('\u226D'), 1)

        self.assertRaises(TypeError, self.db.mirrored)
        self.assertRaises(TypeError, self.db.mirrored, 'xx')

    def test_combining(self):
        self.assertEqual(self.db.combining('\uFFFE'), 0)
        self.assertEqual(self.db.combining('a'), 0)
        self.assertEqual(self.db.combining('\u20e1'), 230)
        self.assertEqual(self.db.combining('\U00020000'), 0)

        # New in 4.1.0
        self.assertEqual(self.db.combining('\u0350'), 230)
        # New in 9.0.0
        self.assertEqual(self.db.combining('\U0001e94a'), 7)
        # New in 13.0.0
        self.assertEqual(self.db.combining('\u1abf'), 220)
        self.assertEqual(self.db.combining('\U00016ff1'), 6)
        # New in 14.0.0
        self.assertEqual(self.db.combining('\u0c3c'), 7)
        self.assertEqual(self.db.combining('\U0001e2ae'), 230)
        # New in 15.0.0
        self.assertEqual(self.db.combining('\U00010efd'), 220)
        # New in 16.0.0
        self.assertEqual(self.db.combining('\u0897'), 230)
        # New in 17.0.0
        self.assertEqual(self.db.combining('\u1ACF'), 230)

        self.assertRaises(TypeError, self.db.combining)
        self.assertRaises(TypeError, self.db.combining, 'xx')

    def test_no_names_in_pua(self):
        puas = [*range(0xe000, 0xf8ff),
                *range(0xf0000, 0xfffff),
                *range(0x100000, 0x10ffff)]
        for i in puas:
            char = chr(i)
            self.assertRaises(ValueError, self.db.name, char)

    def test_long_combining_mark_run(self):
        # gh-149079: avoid quadratic canonical ordering.
        payload = "a" + ("\u0300\u0327" * 32)
        nfd = "a" + ("\u0327" * 32) + ("\u0300" * 32)
        nfc = "\u00e0" + ("\u0327" * 32) + ("\u0300" * 31)

        self.assertEqual(self.db.normalize("NFD", payload), nfd)
        self.assertEqual(self.db.normalize("NFKD", payload), nfd)
        self.assertEqual(self.db.normalize("NFC", payload), nfc)
        self.assertEqual(self.db.normalize("NFKC", payload), nfc)

    def test_combining_mark_run_fast_paths(self):
        # gh-149079: cover short runs and already-sorted long runs.
        short_payload = "a" + ("\u0300\u0327" * 9) + "\u0300"
        short_nfd = "a" + ("\u0327" * 9) + ("\u0300" * 10)
        short_nfc = "\u00e0" + ("\u0327" * 9) + ("\u0300" * 9)
        long_sorted = "a" + ("\u0327" * 30) + ("\u0300" * 30)
        long_sorted_nfc = "\u00e0" + ("\u0327" * 30) + ("\u0300" * 29)

        self.assertEqual(self.db.normalize("NFD", short_payload), short_nfd)
        self.assertEqual(self.db.normalize("NFKD", short_payload), short_nfd)
        self.assertEqual(self.db.normalize("NFC", short_payload), short_nfc)
        self.assertEqual(self.db.normalize("NFKC", short_payload), short_nfc)
        self.assertEqual(self.db.normalize("NFD", long_sorted), long_sorted)
        self.assertEqual(self.db.normalize("NFKD", long_sorted), long_sorted)
        self.assertEqual(self.db.normalize("NFC", long_sorted), long_sorted_nfc)
        self.assertEqual(self.db.normalize("NFKC", long_sorted), long_sorted_nfc)

    def test_pr29(self):
        # http://www.unicode.org/review/pr-29.html
        # See issues #1054943 and #10254.
        composed = ("\u0b47\u0300\u0b3e", "\u1100\u0300\u1161",
                    'Li\u030dt-s\u1e73\u0301',
                    '\u092e\u093e\u0930\u094d\u0915 \u091c\u093c'
                    + '\u0941\u0915\u0947\u0930\u092c\u0930\u094d\u0917',
                    '\u0915\u093f\u0930\u094d\u0917\u093f\u091c\u093c'
                    + '\u0938\u094d\u0924\u093e\u0928')
        for text in composed:
            self.assertEqual(self.db.normalize('NFC', text), text)

    def test_issue10254(self):
        # Crash reported in #10254
        a = 'C\u0338' * 20  + 'C\u0327'
        b = 'C\u0338' * 20  + '\xC7'
        self.assertEqual(self.db.normalize('NFC', a), b)

    def test_issue29456(self):
        # Fix #29456
        u1176_str_a = '\u1100\u1176\u11a8'
        u1176_str_b = '\u1100\u1176\u11a8'
        u11a7_str_a = '\u1100\u1175\u11a7'
        u11a7_str_b = '\uae30\u11a7'
        u11c3_str_a = '\u1100\u1175\u11c3'
        u11c3_str_b = '\uae30\u11c3'
        self.assertEqual(self.db.normalize('NFC', u1176_str_a), u1176_str_b)
        self.assertEqual(self.db.normalize('NFC', u11a7_str_a), u11a7_str_b)
        self.assertEqual(self.db.normalize('NFC', u11c3_str_a), u11c3_str_b)


    def test_cjk_unified_ideograph_names(self):
        # Test that the generated name table covers all CJK ranges by checking
        # that name() and lookup() work for the first and last codepoint of
        # each range, including the Unicode 18 Extension D addition.
        cjk_ranges = [
            (0x3400, 0x4DBF),    # CJK Ideograph Extension A
            (0x4E00, 0x9FFF),    # CJK Ideograph
            (0x20000, 0x2A6DF),  # CJK Ideograph Extension B
            (0x2A700, 0x2B73F),  # CJK Ideograph Extension C
            (0x2B740, 0x2B81E),  # CJK Ideograph Extension D
            (0x2B820, 0x2CEAD),  # CJK Ideograph Extension E
            (0x2CEB0, 0x2EBE0),  # CJK Ideograph Extension F
            (0x2EBF0, 0x2EE5D),  # CJK Ideograph Extension I
            (0x30000, 0x3134A),  # CJK Ideograph Extension G
            (0x31350, 0x323AF),  # CJK Ideograph Extension H
            (0x323B0, 0x33479),  # CJK Ideograph Extension J
        ]
        for start, end in cjk_ranges:
            for cp in (start, end):
                expected_name = "CJK UNIFIED IDEOGRAPH-%X" % cp
                char = chr(cp)
                self.assertEqual(self.db.name(char), expected_name)
                self.assertEqual(self.db.lookup(expected_name), char)

    def test_name(self):
        name = self.db.name
        self.assertRaises(ValueError, name, '\0')
        self.assertRaises(ValueError, name, '\n')
        self.assertRaises(ValueError, name, '\x1F')
        self.assertRaises(ValueError, name, '\x7F')
        self.assertRaises(ValueError, name, '\x9F')
        self.assertRaises(ValueError, name, '\uFFFE')
        self.assertRaises(ValueError, name, '\uFFFF')
        self.assertRaises(ValueError, name, '\U0010FFFF')
        self.assertEqual(name('\U0010FFFF', 42), 42)

        self.assertEqual(name(' '), 'SPACE')
        self.assertEqual(name('1'), 'DIGIT ONE')
        self.assertEqual(name('A'), 'LATIN CAPITAL LETTER A')
        self.assertEqual(name('\xA0'), 'NO-BREAK SPACE')
        self.assertEqual(name('\u0221', None), 'LATIN SMALL LETTER D WITH CURL')
        self.assertEqual(name('\u3400'), 'CJK UNIFIED IDEOGRAPH-3400')
        self.assertEqual(name('\u9FA5'), 'CJK UNIFIED IDEOGRAPH-9FA5')
        self.assertEqual(name('\uAC00'), 'HANGUL SYLLABLE GA')
        self.assertEqual(name('\uD7A3'), 'HANGUL SYLLABLE HIH')
        self.assertEqual(name('\uF900'), 'CJK COMPATIBILITY IDEOGRAPH-F900')
        self.assertEqual(name('\uFA6A'), 'CJK COMPATIBILITY IDEOGRAPH-FA6A')
        self.assertEqual(name('\uFBF9'),
                         'ARABIC LIGATURE UIGHUR KIRGHIZ YEH WITH HAMZA '
                         'ABOVE WITH ALEF MAKSURA ISOLATED FORM')
        self.assertEqual(name('\U00013460', None), 'EGYPTIAN HIEROGLYPH-13460')
        self.assertEqual(name('\U000143FA', None), 'EGYPTIAN HIEROGLYPH-143FA')
        self.assertEqual(name('\U00017000', None), 'TANGUT IDEOGRAPH-17000')
        self.assertEqual(name('\U00018B00', None),
                         'KHITAN SMALL SCRIPT CHARACTER-18B00')
        self.assertEqual(name('\U00018CD5', None),
                         'KHITAN SMALL SCRIPT CHARACTER-18CD5')
        self.assertEqual(name('\U00018CFF', None),
                         'KHITAN SMALL SCRIPT CHARACTER-18CFF')
        self.assertEqual(name('\U00018D1E', None), 'TANGUT IDEOGRAPH-18D1E')
        self.assertEqual(name('\U0001B170', None), 'NUSHU CHARACTER-1B170')
        self.assertEqual(name('\U0001B2FB', None), 'NUSHU CHARACTER-1B2FB')
        self.assertEqual(name('\U0001FBA8', None),
                         'BOX DRAWINGS LIGHT DIAGONAL UPPER CENTRE TO '
                         'MIDDLE LEFT AND MIDDLE RIGHT TO LOWER CENTRE')
        self.assertEqual(name('\U0002A6D6'), 'CJK UNIFIED IDEOGRAPH-2A6D6')
        self.assertEqual(name('\U0002FA1D'), 'CJK COMPATIBILITY IDEOGRAPH-2FA1D')
        self.assertEqual(name('\U00033479', None), 'CJK UNIFIED IDEOGRAPH-33479')

    def test_lookup_nonexistant(self):
        # just make sure that lookup can fail
        for nonexistent in [
            "LATIN SMLL LETR A",
            "OPEN HANDS SIGHS",
            "DREGS",
            "HANDBUG",
            "MODIFIER LETTER CYRILLIC SMALL QUESTION MARK",
            "???",
            "CJK UNIFIED IDEOGRAPH-03400",
            "CJK UNIFIED IDEOGRAPH-020000",
            "CJK UNIFIED IDEOGRAPH-33FF",
            "CJK UNIFIED IDEOGRAPH-F900",
            "CJK UNIFIED IDEOGRAPH-13460",
            "CJK UNIFIED IDEOGRAPH-17000",
            "CJK UNIFIED IDEOGRAPH-18B00",
            "CJK UNIFIED IDEOGRAPH-1B170",
            "CJK COMPATIBILITY IDEOGRAPH-3400",
            "TANGUT IDEOGRAPH-3400",
            "HANGUL SYLLABLE AC00",
        ]:
            self.assertRaises(KeyError, self.db.lookup, nonexistent)

    def test_hangul_syllables(self):
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE GA"), "\uac00")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE GGWEOSS"), "\uafe8")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE DOLS"), "\ub3d0")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE RYAN"), "\ub7b8")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE MWIK"), "\ubba0")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE BBWAEM"), "\ubf88")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE SSEOL"), "\uc370")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE YI"), "\uc758")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE JJYOSS"), "\ucb40")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE KYEOLS"), "\ucf28")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE PAN"), "\ud310")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE HWEOK"), "\ud6f8")
        self.assertEqual(self.db.lookup("HANGUL SYLLABLE HIH"), "\ud7a3")

        self.assertEqual(self.db.lookup("haNGul SYllABle WAe"), '\uc65c')
        self.assertEqual(self.db.lookup("HAngUL syLLabLE waE"), '\uc65c')

        self.assertRaises(ValueError, self.db.name, "\ud7a4")

    def test_tangut_ideographs(self):
        self.assertEqual(self.db.lookup("TANGUT IDEOGRAPH-17000"), "\U00017000")
        self.assertEqual(self.db.lookup("TANGUT IDEOGRAPH-187FF"), "\U000187ff")
        self.assertEqual(self.db.lookup("TANGUT IDEOGRAPH-18D00"), "\U00018D00")
        self.assertEqual(self.db.lookup("TANGUT IDEOGRAPH-18D1E"), "\U00018d1e")
        self.assertEqual(self.db.lookup("tangut ideograph-18d1e"), "\U00018d1e")

    def test_all_names(self):
        filename = 'DerivedName-%s.txt' % self.db.unidata_version
        path = Path(__file__).with_name('data') / filename
        with path.open(encoding='utf-8') as testdata:
            self.assertEqual(testdata.readline().strip(), '# ' + filename)
            self.run_name_tests(testdata)

    def run_name_tests(self, testdata):
        names_ref = {}

        def parse_cp(s):
            return int(s, 16)

        # Parse data
        for line in testdata:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            raw_cp, name = line.split("; ")
            # Check for a range
            if ".." in raw_cp:
                cp1, cp2 = map(parse_cp, raw_cp.split(".."))
                # remove ‘*’ at the end
                assert name[-1] == '*', (raw_cp, name)
                name = name[:-1]
                for cp in range(cp1, cp2 + 1):
                    names_ref[cp] = f"{name}{cp:04X}"
            elif name[-1] == '*':
                cp = parse_cp(raw_cp)
                name = name[:-1]
                names_ref[cp] = f"{name}{cp:04X}"
            else:
                assert '*' not in name, (raw_cp, name)
                cp = parse_cp(raw_cp)
                names_ref[cp] = name

        for cp in range(0, sys.maxunicode + 1):
            self.assertEqual(self.db.name(chr(cp), None), names_ref.get(cp))

    def test_east_asian_width(self):
        eaw = self.db.east_asian_width
        self.assertRaises(TypeError, eaw, b'a')
        self.assertRaises(TypeError, eaw, bytearray())
        self.assertRaises(TypeError, eaw, '')
        self.assertRaises(TypeError, eaw, 'ra')
        self.assertEqual(eaw('\x1e'), 'N')
        self.assertEqual(eaw('\x20'), 'Na')
        self.assertEqual(eaw('\uC894'), 'W')
        self.assertEqual(eaw('\uFF66'), 'H')
        self.assertEqual(eaw('\uFF1F'), 'F')
        self.assertEqual(eaw('\u2010'), 'A')
        self.assertEqual(eaw('\U00020000'), 'W')

    def test_east_asian_width_unassigned(self):
        eaw = self.db.east_asian_width
        # unassigned
        for char in '\u0530\u0ecf\u10c6\u20fc\uaaca\U000107c0\U000115f2':
            self.assertEqual(eaw(char), 'N')
            self.assertIs(self.db.name(char, None), None)

        # unassigned but reserved for CJK
        for char in '\uFA6E\uFADA\U0002A6E0\U0002FA20\U0003134B\U0003FFFD':
            self.assertEqual(eaw(char), 'W')
            self.assertIs(self.db.name(char, None), None)

        # private use areas
        for char in '\uE000\uF800\U000F0000\U000FFFEE\U00100000\U0010FFF0':
            self.assertEqual(eaw(char), 'A')
            self.assertIs(self.db.name(char, None), None)

    def test_east_asian_width_9_0_changes(self):
        self.assertEqual(self.db.ucd_3_2_0.east_asian_width('\u231a'), 'N')
        self.assertEqual(self.db.east_asian_width('\u231a'), 'W')

class UnicodeMiscTest(UnicodeDatabaseTest):

    # NOTE: this test is specific to CPython and is disabled in unicodedata2
#     def test_failed_import_during_compiling(self):
#         # Issue 4367
#         # Decoding \N escapes requires the unicodedata module. If it can't be
#         # imported, we shouldn't segfault.
#
#         # This program should raise a SyntaxError in the eval.
#         code = "import sys;" \
#             "sys.modules['unicodedata'] = None;" \
#             """eval("'\\\\N{SOFT HYPHEN}'")"""
#         # We use a separate process because the unicodedata module may already
#         # have been loaded in this process.
#         result = script_helper.assert_python_failure("-c", code)
#         error = "SyntaxError: (unicode error) \\N escapes not supported " \
#             "(can't load unicodedata module)"
#         self.assertIn(error, result.err.decode("ascii"))

    def test_decimal_numeric_consistent(self):
        # Test that decimal and numeric are consistent,
        # i.e. if a character has a decimal value,
        # its numeric value should be the same.
        count = 0
        for i in range(sys.maxunicode + 1):
            c = chr(i)
            dec = self.db.decimal(c, -1)
            if dec != -1:
                self.assertEqual(dec, self.db.numeric(c))
                count += 1
        self.assertTrue(count >= 10) # should have tested at least the ASCII digits

    def test_digit_numeric_consistent(self):
        # Test that digit and numeric are consistent,
        # i.e. if a character has a digit value,
        # its numeric value should be the same.
        count = 0
        for i in range(sys.maxunicode + 1):
            c = chr(i)
            dec = self.db.digit(c, -1)
            if dec != -1:
                self.assertEqual(dec, self.db.numeric(c))
                count += 1
        self.assertTrue(count >= 10) # should have tested at least the ASCII digits

    def test_bug_1704793(self):
        self.assertEqual(self.db.lookup("GOTHIC LETTER FAIHU"), '\U00010346')

    def test_ucd_510(self):
        import unicodedata2
        # In UCD 5.1.0, a mirrored property changed wrt. UCD 3.2.0
        self.assertTrue(unicodedata2.mirrored("\u0f3a"))
        self.assertTrue(not unicodedata2.ucd_3_2_0.mirrored("\u0f3a"))
        # Also, we now have two ways of representing
        # the upper-case mapping: as delta, or as absolute value
        self.assertTrue("a".upper()=='A')
        self.assertTrue("\u1d79".upper()=='\ua77d')
        self.assertTrue(".".upper()=='.')

    def test_bug_5828(self):
        self.assertEqual("\u1d79".lower(), "\u1d79")
        # Only U+0000 should have U+0000 as its upper/lower/titlecase variant
        self.assertEqual(
            [
                c for c in range(sys.maxunicode+1)
                if "\x00" in chr(c).lower()+chr(c).upper()+chr(c).title()
            ],
            [0]
        )

    def test_bug_4971(self):
        # LETTER DZ WITH CARON: DZ, Dz, dz
        self.assertEqual("\u01c4".title(), "\u01c5")
        self.assertEqual("\u01c5".title(), "\u01c5")
        self.assertEqual("\u01c6".title(), "\u01c5")

    def test_linebreak_7643(self):
        for i in range(0x10000):
            lines = (chr(i) + 'A').splitlines()
            if i in (0x0a, 0x0b, 0x0c, 0x0d, 0x85,
                     0x1c, 0x1d, 0x1e, 0x2028, 0x2029):
                self.assertEqual(len(lines), 2,
                                 r"\u%.4x should be a linebreak" % i)
            else:
                self.assertEqual(len(lines), 1,
                                 r"\u%.4x should not be a linebreak" % i)

    def test_normalize_return_type(self):
        # gh-129569: normalize() return type must always be str
        normalize = self.db.normalize

        class MyStr(str):
            pass

        normalization_forms = ("NFC", "NFKC", "NFD", "NFKD")
        input_strings = (
            # normalized strings
            "",
            "ascii",
            # unnormalized strings
            "\u1e0b\u0323",
            "\u0071\u0307\u0323",
        )

        for form in normalization_forms:
            for input_str in input_strings:
                with self.subTest(form=form, input_str=input_str):
                    self.assertIs(type(normalize(form, input_str)), str)
                    self.assertIs(type(normalize(form, MyStr(input_str))), str)


class NormalizationTest(UnicodeDatabaseTest):
    # Adapted from CPython's Lib/test/test_unicodedata.py (9ab004d41e).
    # Setup downloads the data; never skip it. unicodedata2 has no is_normalized.
    @staticmethod
    def unistr(data):
        data = [int(x, 16) for x in data.split(" ")]
        return "".join([chr(x) for x in data])

    def test_normalization(self):
        self.check_normalization(self.db)

    def test_normalization_3_2_0(self):
        self.check_normalization(self.db.ucd_3_2_0)

    def check_normalization(self, ucd):
        filename = 'NormalizationTest-%s.txt' % ucd.unidata_version
        path = Path(__file__).with_name('data') / filename
        with path.open(encoding='utf-8') as testdata:
            self.assertEqual(testdata.readline().strip(), '# ' + filename)
            self.run_normalization_tests(testdata, ucd)

    def run_normalization_tests(self, testdata, ucd):
        part = None
        part1_data = set()

        NFC = partial(ucd.normalize, "NFC")
        NFKC = partial(ucd.normalize, "NFKC")
        NFD = partial(ucd.normalize, "NFD")
        NFKD = partial(ucd.normalize, "NFKD")

        for line in testdata:
            if '#' in line:
                line = line.split('#')[0]
            line = line.strip()
            if not line:
                continue
            if line.startswith("@Part"):
                part = line.split()[0]
                continue
            c1,c2,c3,c4,c5 = [self.unistr(x) for x in line.split(';')[:-1]]

            # Perform tests
            self.assertTrue(c2 ==  NFC(c1) ==  NFC(c2) ==  NFC(c3), line)
            self.assertTrue(c4 ==  NFC(c4) ==  NFC(c5), line)
            self.assertTrue(c3 ==  NFD(c1) ==  NFD(c2) ==  NFD(c3), line)
            self.assertTrue(c5 ==  NFD(c4) ==  NFD(c5), line)
            self.assertTrue(c4 == NFKC(c1) == NFKC(c2) == \
                            NFKC(c3) == NFKC(c4) == NFKC(c5),
                            line)
            self.assertTrue(c5 == NFKD(c1) == NFKD(c2) == \
                            NFKD(c3) == NFKD(c4) == NFKD(c5),
                            line)

            # Record part 1 data
            if part == "@Part1":
                part1_data.add(c1)

        # Perform tests for all other data
        for X in map(chr, range(sys.maxunicode + 1)):
            if X in part1_data:
                continue
            self.assertTrue(X == NFC(X) == NFD(X) == NFKC(X) == NFKD(X), ord(X))

    def test_edge_cases(self):
        self.assertRaises(TypeError, self.db.normalize)
        self.assertRaises(ValueError, self.db.normalize, 'unknown', 'xx')
        self.assertEqual(self.db.normalize('NFKC', ''), '')

    def test_bug_834676(self):
        # Check for bug 834676
        self.db.normalize('NFC', '\ud55c\uae00')

if __name__ == "__main__":
    unittest.main()
