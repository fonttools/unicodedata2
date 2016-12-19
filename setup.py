import sys
from setuptools import setup, Extension

if sys.version_info < (3,):
    type = 'py2'
else:
    type = 'py3'

module1 = Extension('unicodedata2',
                    sources = ['./unicodedata2/' + type + '/unicodedata.c',
                               './unicodedata2/unicodectype.c'],
                    include_dirs = ['./unicodedata2/' + type, './unicodedata2/'],
)

setup (name = "unicodedata2",
       version = "9.0.0-4",
       description = "Unicodedata backport for python 2/3 updated to the latest unicode version.",
       ext_modules = [module1],
       author="Mike Kaplinskiy",
       author_email="mike.kaplinskiy@gmail.com",
       download_url="http://github.com/mikekap/unicodedata2",
       license="Apache License 2.0",
       platforms=['any'],
       url="http://github.com/mikekap/unicodedata2",
       test_suite="tests",
)
