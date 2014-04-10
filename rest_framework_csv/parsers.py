import csv
import codecs
import io

from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from rest_framework_csv.orderedrows import OrderedRows


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    # csv.py doesn't do Unicode; encode temporarily:
    csv_reader = csv.reader(charset_encoder(unicode_csv_data, charset=charset),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode back to Unicode, cell by cell:
        yield [cell.decode(charset) for cell in row]

def charset_encoder(unicode_csv_data, charset='utf-8'):
    for line in unicode_csv_data:
        yield line.encode(charset)

def universal_newlines(stream):
    for intermediate_line in stream:
        # It's possible that the stream was not opened in universal
        # newline mode. If not, we may have a single "row" that has a
        # bunch of carriage return (\r) characters that should act as
        # newlines. For that case, lets call splitlines on the row. If
        # it doesn't have any newlines, it will return a list of just
        # the row itself.
        for line in intermediate_line.splitlines():
            yield line


class CSVParser(BaseParser):
    """
    Parses CSV serialized data.

    The parser assumes the first line contains the column names.
    """

    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        delimiter = parser_context.get('delimiter', ',')

        try:
            encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
            rows = unicode_csv_reader(universal_newlines(stream), delimiter=delimiter, charset=encoding)
            data = OrderedRows(next(rows))
            for row in rows:
                row_data = dict(zip(data.header, row))
                data.append(row_data)
            return data
        except Exception as exc:
            raise ParseError('CSV parse error - %s' % str(exc))
