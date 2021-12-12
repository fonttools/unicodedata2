[![Githun CI Status](https://github.com/fonttools/unicodedata2/workflows/Build%20+%20Deploy/badge.svg)](https://github.com/fonttools/unicodedata2/actions?query=workflow%3A%22Build+%2B+Deploy%22)
[![PyPI](https://img.shields.io/pypi/v/unicodedata2.svg)](https://pypi.org/project/unicodedata2/)

unicodedata2
============

[unicodedata] backport/updates.

The versions of this package match Unicode versions, so unicodedata2==13.0.0 is data from Unicode 13.0.0.

Pre-compiled wheel packages are available on [PyPI] and can be installed via pip.

[unicodedata]: https://docs.python.org/3/library/unicodedata.html
[PyPI]: https://pypi.org/project/unicodedata2/


Testing
=======

We run the tests using `tox`. This can be installed as usual with `pip install tox`.

Without any options, `tox` will run the tests against the current python version where
`tox` itself was installed:

To run tests against a specific python version you can use the `-e` option followed by
a tox environment name. E.g. `-e py38` will run tests against Python 3.8.
For more info, check `tox`'s [documentation](https://tox.readthedocs.io/en/latest/).
