from setuptools import setup, Extension

module1 = Extension('unicodedata2',
                    sources = ['./unicodedata2/unicodedata.c'],
                    include_dirs = ['./unicodedata2'],
)

setup (name = "unicodedata2",
       version = "9.0.0",
       description = "Unicodedata backport for python 2 updated to the latest unicode version.",
       ext_modules = [module1],
       author="Mike Kaplinskiy",
       author_email="mike.kaplinskiy@gmail.com",
       download_url="http://github.com/mikekap/unicodedata2",
       license="Apache License 2.0",
       platforms=['any'],
       url="http://github.com/mikekap/unicodedata2",
       test_suite="tests",
)
