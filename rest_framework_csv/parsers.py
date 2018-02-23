import unicodecsv as csv
#import csv
import codecs
import io
import six

from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from rest_framework_csv.orderedrows import OrderedRows


def unicode_csv_reader(csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    csv_reader = csv.reader(csv_data, dialect=dialect, encoding=charset, **kwargs)
    for row in csv_reader:
        yield row

def universal_newlines(stream):
    # It's possible that the stream was not opened in universal
    # newline mode. If not, we may have a single "row" that has a
    # bunch of carriage return (\r) characters that should act as
    # newlines. For that case, lets call splitlines on the row. If
    # it doesn't have any newlines, it will return a list of just
    # the row itself.
    for line in stream.splitlines():
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
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            strdata = stream.read()
            binary = universal_newlines(strdata)
            rows = unicode_csv_reader(binary, delimiter=delimiter, charset=encoding)
            data = OrderedRows(next(rows))
            for row in rows:
                row_data = dict(zip(data.header, row))
                data.append(row_data)
            return data
        except Exception as exc:
            raise ParseError('CSV parse error - %s' % str(exc))

