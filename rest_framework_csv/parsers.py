import csv
import codecs
import io
import six
import xlrd

from django.conf import settings
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from rest_framework_csv.orderedrows import OrderedRows


def preprocess_stream(stream, charset):
    if six.PY2:
        # csv.py doesn't do Unicode; encode temporarily:
        return (chunk.encode(charset) for chunk in stream)
    else:
        return stream

def postprocess_row(row, charset):
    if six.PY2:
        # decode back to Unicode, cell by cell:
        return [cell.decode(charset) for cell in row]
    else:
        return row

def unicode_csv_reader(csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    csv_data = preprocess_stream(csv_data, charset)
    csv_reader = csv.reader(csv_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield postprocess_row(row, charset)

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

class HierarchicalCSVParser(BaseParser):
    """
    Parses CSV serialized data into hierarchical structure.

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
                hierarchical_data = self._csv_convert(row_data)
                data.append(hierarchical_data)
            return data
        except Exception as exc:
            raise ParseError('HierarchicalCSV parse error - %s' % str(exc))

    def _csv_convert(self,flat_data):
        first_level_keys = {key.split(".")[0] for key in flat_data.keys()}
        if list(first_level_keys)[0].isdigit():
            d = []
        else:
            d = {}
        for first_level_key in first_level_keys:                
            # a subset of the dictionary with only the entries with the
            # key: first_level_key.* and non empty value
            subset = {key:value for key, value in flat_data.items() if key.partition(".")[0]==first_level_key and self.must_include(value)}
            if len(subset) > 0:
                at_deepest = subset.keys()[0].partition(".")[1]==''
                if at_deepest:
                    # end of recursivity
                    d.update(subset)
                else:
                    # can go deeper
                    # remove the first_level_key 
                    flat_second_level_subset = {key.partition(".")[2]:value for key, value in subset.items()}
                    second_level_subset = self._csv_convert(flat_second_level_subset)
                    if first_level_key.isdigit():
                        # add to the list
                        d.append(second_level_subset)
                    else:
                        # add to the dictionary
                        d[first_level_key] = second_level_subset
        
        return d
    
    def must_include(self,value):
        # do not include empty unicode
        if isinstance(value, (str,unicode)):
            if len(value)==0:
                return False
        return True
    
class HierarchicalXLSParser(HierarchicalCSVParser):
    """
    Parses XLS serialized data into hierarchical structure.

    The parser assumes the first line contains the column names.
    """

    media_type = 'application/vnd.ms-excel'

    def parse(self, stream, media_type=None, parser_context=None):
        book = xlrd.open_workbook(file_contents=stream,encoding_override='utf-8')
        print "[HierarchicalXLSParser] book encoding: %s" % book.encoding
        sheet = book.sheet_by_index(0)

        data = []
        header = []
        try:
            for row_index in range(sheet.nrows):
                row = []
                for col_index in range(sheet.ncols):
                    if row_index==0:
                        header.append(sheet.cell(row_index,col_index).value)
                    else:
                        row.append(sheet.cell(row_index,col_index).value)
                if row_index!=0:
                    row_data = dict(zip(header, row))
                    hierarchical_data = self._csv_convert(row_data)
                    data.append(hierarchical_data)
            return data
        except Exception as exc:
            raise ParseError('HierarchicalXLS parse error - %s' % str(exc))
        

