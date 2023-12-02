
from .base import Converter
from ...helpers import iterate_files, get_ip

from pandas import ExcelWriter


class ExcelConverter(Converter):

    fields = [
        'port',
        'timestamp',
        'data',
        'hostnames',
        'org',
        'isp',
        'location.country_name',
        'location.country_code',
        'location.city',
        'os',
        'asn',
        'transport',
        'product',
        'version',

        'http.server',
        'http.title',
    ]

    field_names = {
        'org': 'Organization',
        'isp': 'ISP',
        'location.country_code': 'Country ISO Code',
        'location.country_name': 'Country',
        'location.city': 'City',
        'os': 'OS',
        'asn': 'ASN',

        'http.server': 'Web Server',
        'http.title': 'Website Title',
    }

    def process(self, files, file_size):
        engine_kwargs = dict()

        with ExcelWriter(f"{self.basename}.xlsx", engine="xlsxwriter") as writer:
            if file_size > 4e9:
                engine_kwargs['use_zip64'] = True

            self.df.to_excel(writer, index=False, header=True, engine_kwargs=engine_kwargs)
