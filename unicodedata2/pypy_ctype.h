#ifndef __PYPY_SHIMS_H__
#define __PYPY_SHIMS_H__

#ifdef PYPY_VERSION

PyAPI_DATA(const unsigned char) _Py_ctype_toupper[256];
#define Py_TOUPPER(c) (_Py_ctype_toupper[Py_CHARMASK(c)])

#endif

#endif
