#ifndef __UNICODEDATA2_COMPAT_H__
#define __UNICODEDATA2_COMPAT_H__

/*
 * Compatibility shims
 */


/* ----------------------------------------------------------------------- *
 * Update for Python 3.11 - Contributed by Victor Stinner in bpo-39573.
 * Compatibility macro for older Python versions.
 * ----------------------------------------------------------------------- */
#if PY_VERSION_HEX < 0x030900A4 && !defined(Py_SET_TYPE)
static inline void _Py_SET_TYPE(PyObject *ob, PyTypeObject *type)
{ ob->ob_type = type; }
#define Py_SET_TYPE(ob, type) _Py_SET_TYPE((PyObject*)(ob), type)
#endif


#ifdef PYPY_VERSION
#include "pypy_ctype.h"
typedef Py_ssize_t Py_ssize_clean_t;
#endif

#endif
