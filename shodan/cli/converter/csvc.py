
from .base import Converter

try:
    # python 3.x: Import ABC from collections.abc
    from collections.abc import MutableMapping
except ImportError:
    # Python 2.x: Import ABC from collections
    from collections import MutableMapping


class CsvConverter(Converter):

    fields = [
        'data',
        'hostnames',
        'ip',
        'ip_str',
        'ipv6',
        'org',
        'isp',
        'location.country_code',
        'location.city',
        'location.country_name',
        'location.latitude',
        'location.longitude',
        'os',
        'asn',
        'port',
        'tags',
        'timestamp',
        'transport',
        'product',
        'version',
        'vulns',

        'ssl.cipher.version',
        'ssl.cipher.bits',
        'ssl.cipher.name',
        'ssl.alpn',
        'ssl.versions',
        'ssl.cert.serial',
        'ssl.cert.fingerprint.sha1',
        'ssl.cert.fingerprint.sha256',

        'html',
        'title',
    ]

    def process(self, files, file_size):
        try:
            self.df.to_csv(f'{self.basename}.csv', index=False)
        except Exception as e:
            raise RuntimeError(f"Error converting file to csv.\n{e}")
