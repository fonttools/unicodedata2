"""Download version-matched normalization data before running the tests."""

from pathlib import Path
import re
from urllib.request import Request, urlopen


def main():
    tests_dir = Path(__file__).resolve().parent
    header = tests_dir.parent / 'unicodedata2' / 'unicodedata_db.h'
    match = re.search(r'^#define UNIDATA_VERSION "([^"]+)"',
                      header.read_text(encoding='utf-8'), re.MULTILINE)
    if match is None:
        raise ValueError('Cannot find UNIDATA_VERSION in %s' % header)

    data_dir = tests_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    for version in (match.group(1), '3.2.0'):
        filename = 'NormalizationTest-%s.txt' % version
        if version == '3.2.0':
            url = 'https://www.unicode.org/Public/3.2-Update/' + filename
        else:
            url = ('https://www.unicode.org/Public/%s/ucd/NormalizationTest.txt'
                   % version)
        request = Request(url, headers={'User-Agent': 'unicodedata2'})
        with urlopen(request, timeout=60) as response:
            data = response.read()
        if data.decode('utf-8').splitlines()[:1] != ['# ' + filename]:
            raise ValueError('Unexpected version header in %s' % url)
        (data_dir / filename).write_bytes(data)
        print('Downloaded %s' % filename)


if __name__ == '__main__':
    main()
