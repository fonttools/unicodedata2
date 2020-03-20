[![Travis Build Status](https://travis-ci.org/mikekap/unicodedata2.svg?branch=master)](https://travis-ci.org/mikekap/unicodedata2)

unicodedata2
============

[unicodedata] backport/updates to Python 3 and Python 2.

The versions of this package match Unicode versions, so unicodedata2==13.0.0 is data from Unicode 13.0.0.
Additionally this backports support for named aliases and named sequences to Python 2.

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
