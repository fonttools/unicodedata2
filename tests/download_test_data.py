"""Download version-matched Unicode data before running the tests."""

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
    version = match.group(1)
    base_url = 'https://www.unicode.org/Public/'
    downloads = [
        ('NormalizationTest-%s.txt' % version,
         '%s/ucd/NormalizationTest.txt' % version),
        ('NormalizationTest-3.2.0.txt',
         '3.2-Update/NormalizationTest-3.2.0.txt'),
        ('DerivedName-%s.txt' % version,
         '%s/ucd/extracted/DerivedName.txt' % version),
    ]
    for filename, remote_path in downloads:
        url = base_url + remote_path
        request = Request(url, headers={'User-Agent': 'unicodedata2'})
        with urlopen(request, timeout=60) as response:
            data = response.read()
        if data.decode('utf-8').splitlines()[:1] != ['# ' + filename]:
            raise ValueError('Unexpected version header in %s' % url)
        (data_dir / filename).write_bytes(data)
        print('Downloaded %s' % filename)


if __name__ == '__main__':
    main()
