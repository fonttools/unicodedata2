[![Githun CI Status](https://github.com/fonttools/unicodedata2/workflows/Build%20+%20Deploy/badge.svg)](https://github.com/fonttools/unicodedata2/actions?query=workflow%3A%22Build+%2B+Deploy%22)
[![PyPI](https://img.shields.io/pypi/v/unicodedata2.svg)](https://pypi.org/project/unicodedata2/)

unicodedata2
============

[unicodedata] backport/updates. Currently supports Unicode 18.0.0.

Requires Python 3.9 or newer.

The versions of this package match Unicode versions, so unicodedata2==13.0.0 is data from Unicode 13.0.0.

Pre-compiled wheel packages are available on [PyPI] and can be installed via pip.

[unicodedata]: https://docs.python.org/3/library/unicodedata.html
[PyPI]: https://pypi.org/project/unicodedata2/


Testing
=======

We run the tests using `tox`. This can be installed as usual with `pip install tox`,
or with `pip install --group dev` (pip 25.1 or newer) to pick it up from
`pyproject.toml`.

Tox and CI download the version-matched Unicode normalization data before
running tests. Download failures stop the run. Before running `pytest` directly,
run `python tests/download_test_data.py` once. The downloaded files are not
included in source distributions or wheels.

Without any options, `tox` will run the tests against all of the library's
target Python versions. Any missing versions will be skipped.

To run tests against a specific python version you can use the `-e` option followed by
a tox environment name. E.g. `-e py39` will run tests against Python 3.9.
For more info, check `tox`'s [documentation](https://tox.readthedocs.io/en/latest/).
