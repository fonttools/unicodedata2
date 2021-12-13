import sys
from setuptools import setup, Extension

# concatenate README.md and CHANGELOG.md into long_description so they are
# displayed on the unicodedata2 project page on PyPI
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
long_description += "\nChangelog\n=========\n"
with open("CHANGELOG.md", "r", encoding="utf-8") as changelog:
    long_description += changelog.read()

module_sources = [
    "./unicodedata2/unicodedata.c",
    "./unicodedata2/unicodectype.c",
]

is_pypy = hasattr(sys, "pypy_version_info")
if is_pypy:
    module_sources.append("./unicodedata2/pypy_ctype.c")

module1 = Extension(
    "unicodedata2",
    sources=module_sources,
    include_dirs=["./unicodedata2/"],
)

setup(
    name="unicodedata2",
    version="14.0.0",
    description="Unicodedata backport updated to the latest Unicode version.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[module1],
    author="Mike Kaplinskiy",
    author_email="mike.kaplinskiy@gmail.com",
    download_url="http://github.com/fonttools/unicodedata2",
    license="Apache License 2.0",
    platforms=["any"],
    url="http://github.com/fonttools/unicodedata2",
    test_suite="tests",
    extras_require={
        "testing": [
            "pytest",
            "coverage",
            "pytest-xdist",
            "pytest-randomly",
        ],
    },
)
