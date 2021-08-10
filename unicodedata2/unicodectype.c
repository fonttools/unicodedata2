/*
   Unicode character type helpers.

   Written by Marc-Andre Lemburg (mal@lemburg.com).
   Modified for Python 2.0 by Fredrik Lundh (fredrik@pythonware.com)

   Copyright (c) Corporation for National Research Initiatives.

*/

#include "Python.h"

#define ALPHA_MASK 0x01
#define DECIMAL_MASK 0x02
#define DIGIT_MASK 0x04
#define LOWER_MASK 0x08
#define LINEBREAK_MASK 0x10
#define SPACE_MASK 0x20
#define TITLE_MASK 0x40
#define UPPER_MASK 0x80
#define XID_START_MASK 0x100
#define XID_CONTINUE_MASK 0x200
#define PRINTABLE_MASK 0x400
#define NUMERIC_MASK 0x800
#define CASE_IGNORABLE_MASK 0x1000
#define CASED_MASK 0x2000
#define EXTENDED_CASE_MASK 0x4000

typedef struct {
    /*
       These are either deltas to the character or offsets in
       _PyUnicode_ExtendedCase.
    */
    const int upper;
    const int lower;
    const int title;
    /* Note if more flag space is needed, decimal and digit could be unified. */
    const unsigned char decimal;
    const unsigned char digit;
    const unsigned short flags;
} _PyUnicode_TypeRecord;

#include "unicodetype_db.h"

static const _PyUnicode_TypeRecord *
gettyperecord(Py_UCS4 code)
{
    int index;

    if (code >= 0x110000)
        index = 0;
    else
    {
        index = index1[(code>>SHIFT)];
        index = index2[(index<<SHIFT)+(code&((1<<SHIFT)-1))];
    }

    return &_PyUnicode_TypeRecords[index];
}

#include "pypy_shims.h"

#ifdef PYPY_VERSION

const unsigned char _Py_ctype_toupper[256] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
    0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
    0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f,
    0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
    0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
    0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
    0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f,
    0x60, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
    0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
    0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
    0x58, 0x59, 0x5a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f,
    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
    0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
    0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
    0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f,
    0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7,
    0xa8, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf,
    0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7,
    0xb8, 0xb9, 0xba, 0xbb, 0xbc, 0xbd, 0xbe, 0xbf,
    0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7,
    0xc8, 0xc9, 0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf,
    0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7,
    0xd8, 0xd9, 0xda, 0xdb, 0xdc, 0xdd, 0xde, 0xdf,
    0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7,
    0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef,
    0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7,
    0xf8, 0xf9, 0xfa, 0xfb, 0xfc, 0xfd, 0xfe, 0xff,
};

int _PyUnicode_ToDecimalDigit(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & DECIMAL_MASK) ? ctype->decimal : -1;
}

int _PyUnicode_ToDigit(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & DIGIT_MASK) ? ctype->digit : -1;
}

#endif


/* Returns the titlecase Unicode characters corresponding to ch or just
   ch if no titlecase mapping is known. */

Py_UCS4 _PyUnicode2_ToTitlecase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK)
        return _PyUnicode_ExtendedCase[ctype->title & 0xFFFF];
    return ch + ctype->title;
}

/* Returns 1 for Unicode characters having the category 'Lt', 0
   otherwise. */

int _PyUnicode2_IsTitlecase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & TITLE_MASK) != 0;
}

/* Returns 1 for Unicode characters having the XID_Start property, 0
   otherwise. */

int _PyUnicode2_IsXidStart(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & XID_START_MASK) != 0;
}

/* Returns 1 for Unicode characters having the XID_Continue property,
   0 otherwise. */

int _PyUnicode2_IsXidContinue(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & XID_CONTINUE_MASK) != 0;
}

/* Returns the integer decimal (0-9) for Unicode characters having
   this property, -1 otherwise. */

int _PyUnicode2_ToDecimalDigit(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & DECIMAL_MASK) ? ctype->decimal : -1;
}

int _PyUnicode2_IsDecimalDigit(Py_UCS4 ch)
{
    if (_PyUnicode_ToDecimalDigit(ch) < 0)
        return 0;
    return 1;
}

/* Returns the integer digit (0-9) for Unicode characters having
   this property, -1 otherwise. */

int _PyUnicode2_ToDigit(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & DIGIT_MASK) ? ctype->digit : -1;
}

int _PyUnicode2_IsDigit(Py_UCS4 ch)
{
    if (_PyUnicode_ToDigit(ch) < 0)
        return 0;
    return 1;
}

/* Returns the numeric value as double for Unicode characters having
   this property, -1.0 otherwise. */

int _PyUnicode2_IsNumeric(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & NUMERIC_MASK) != 0;
}

/* Returns 1 for Unicode characters to be hex-escaped when repr()ed,
   0 otherwise.
   All characters except those characters defined in the Unicode character
   database as following categories are considered printable.
      * Cc (Other, Control)
      * Cf (Other, Format)
      * Cs (Other, Surrogate)
      * Co (Other, Private Use)
      * Cn (Other, Not Assigned)
      * Zl Separator, Line ('\u2028', LINE SEPARATOR)
      * Zp Separator, Paragraph ('\u2029', PARAGRAPH SEPARATOR)
      * Zs (Separator, Space) other than ASCII space('\x20').
*/
int _PyUnicode2_IsPrintable(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & PRINTABLE_MASK) != 0;
}

/* Returns 1 for Unicode characters having the category 'Ll', 0
   otherwise. */

int _PyUnicode2_IsLowercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & LOWER_MASK) != 0;
}

/* Returns 1 for Unicode characters having the category 'Lu', 0
   otherwise. */

int _PyUnicode2_IsUppercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & UPPER_MASK) != 0;
}

/* Returns the uppercase Unicode characters corresponding to ch or just
   ch if no uppercase mapping is known. */

Py_UCS4 _PyUnicode2_ToUppercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK)
        return _PyUnicode_ExtendedCase[ctype->upper & 0xFFFF];
    return ch + ctype->upper;
}

/* Returns the lowercase Unicode characters corresponding to ch or just
   ch if no lowercase mapping is known. */

Py_UCS4 _PyUnicode2_ToLowercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK)
        return _PyUnicode_ExtendedCase[ctype->lower & 0xFFFF];
    return ch + ctype->lower;
}

int _PyUnicode2_ToLowerFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK) {
        int index = ctype->lower & 0xFFFF;
        int n = ctype->lower >> 24;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    res[0] = ch + ctype->lower;
    return 1;
}

int _PyUnicode2_ToTitleFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK) {
        int index = ctype->title & 0xFFFF;
        int n = ctype->title >> 24;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    res[0] = ch + ctype->title;
    return 1;
}

int _PyUnicode2_ToUpperFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK) {
        int index = ctype->upper & 0xFFFF;
        int n = ctype->upper >> 24;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    res[0] = ch + ctype->upper;
    return 1;
}

int _PyUnicode2_IsCased(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & CASED_MASK) != 0;
}

int _PyUnicode2_IsCaseIgnorable(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & CASE_IGNORABLE_MASK) != 0;
}

/* Returns 1 for Unicode characters having the category 'Ll', 'Lu', 'Lt',
   'Lo' or 'Lm',  0 otherwise. */

int _PyUnicode2_IsAlpha(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & ALPHA_MASK) != 0;
}
