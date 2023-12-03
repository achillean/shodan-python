
from .base import Converter
from ...helpers import iterate_files, get_ip

from pandas import ExcelWriter
from xlsxwriter import Workbook

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
        row = 1
        col = 3
        engine_kwargs = dict()
        port_count = [{'Port': port, 'Count': self.df['port'].value_counts()[port]}
                      for port in list(self.df['port'].unique())
                      ]

        with ExcelWriter(f"{self.basename}.xlsx", engine="xlsxwriter") as writer:
            if file_size > 4e9:
                engine_kwargs['use_zip64'] = True

            # Raw Shodan Results
            self.df.to_excel(writer, sheet_name="Raw Data", index=False, header=True, engine_kwargs=engine_kwargs)

            # Create Summary
            workbook = writer.book
            bold = workbook.add_format({'bold': 1})

            worksheet = workbook.add_worksheet('Summary')
            worksheet.write(0, 0, 'Total', bold)
            worksheet.write(0, 1, len(self.df.index))
            worksheet.write(0, 3, 'Ports Distribution', bold)

            for record in sorted(port_count, reverse=True, key=lambda d: d['Count']):
                worksheet.write(row, col, record["Port"])
                worksheet.write(row, col + 1, record["Count"])
                row += 1
