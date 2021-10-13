from setuptools import setup, Extension

# concatenate README.md and CHANGELOG.md into long_description so they are
# displayed on the unicodedata2 project page on PyPI
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
long_description += "\nChangelog\n=========\n"
with open("CHANGELOG.md", "r", encoding="utf-8") as changelog:
    long_description += changelog.read()

module1 = Extension(
    "unicodedata2",
    sources=[
        "./unicodedata2/unicodedata.c",
        "./unicodedata2/unicodectype.c",
    ],
    include_dirs=["./unicodedata2/"],
)

setup(
    name="unicodedata2",
    version="13.0.0-2",
    description="Unicodedata backport updated to the latest Unicode version.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[module1],
    author="Mike Kaplinskiy",
    author_email="mike.kaplinskiy@gmail.com",
    download_url="http://github.com/mikekap/unicodedata2",
    license="Apache License 2.0",
    platforms=["any"],
    url="http://github.com/mikekap/unicodedata2",
    test_suite="tests",
)
