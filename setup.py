from setuptools import setup, Extension
import shutil
import sys

module1 = Extension('unicodedata2',
                    sources = ['./unicodedata2/unicodedata.c'],
                    include_dirs = ['./unicodedata2'],
                    extra_compile_args=['-flto'],
                    extra_link_args=['-flto'],
)
					
setup (name = 'unicodedata2',
       version = "7.0.0",
       description = "Unicodedata, but updated to the current unicode version.",
       ext_modules = [module1],
       author="Mike Kaplinskiy",
       author_email="mike.kaplinskiy@gmail.com",
       download_url="http://github.com/mikekap/unicodedata2",
       license="BSD License",
       platforms=['any'],
       url="http://github.com/mikekap/unicodedata2",
)
