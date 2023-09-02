from __future__ import annotations

import csv
import io
from typing import Generator, Iterable

from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from rest_framework_csv.orderedrows import OrderedRows


def unicode_csv_reader(csv_data: Iterable[str], dialect:"csv._DialectLike"=csv.excel,  **kwargs) -> Generator[list[str], None, None]:
    csv_reader = csv.reader(csv_data, dialect=dialect, **kwargs)
    yield from csv_reader

def universal_newlines(stream) -> Generator[str, None, None]:
    # It's possible that the stream was not opened in universal
    # newline mode. If not, we may have a single "row" that has a
    # bunch of carriage return (\r) characters that should act as
    # newlines. For that case, lets call splitlines on the row. If
    # it doesn't have any newlines, it will return a list of just
    # the row itself.
    yield from stream.splitlines()

class CSVParser(BaseParser):
    """
    Parses CSV serialized data.

    The parser assumes the first line contains the column names.
    """

    media_type: str = 'text/csv'

    def parse(self, stream: io.BytesIO | io.StringIO |io.TextIOWrapper, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        delimiter: str = parser_context.get('delimiter', ',')

        try:
            strdata = stream.read()
            binary = universal_newlines(strdata)
            rows = unicode_csv_reader(binary, delimiter=delimiter)
            data = OrderedRows(next(rows))
            for row in rows:
                row_data = dict(zip(data.header, row))
                data.append(row_data)
            return data
        except Exception as exc:
            raise ParseError('CSV parse error - %s' % str(exc))

