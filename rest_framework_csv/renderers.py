from __future__ import unicode_literals
import csv
from rest_framework.renderers import *
from six import StringIO, text_type
from rest_framework_csv.orderedrows import OrderedRows
from rest_framework_csv.misc import Echo

from logging import getLogger
log = getLogger(__name__)

# six versions 1.3.0 and previous don't have PY2
try:
    from six import PY2
except ImportError:
    import sys
    PY2 = sys.version_info[0] == 2


class CSVRenderer(BaseRenderer):
    """
    Renderer which serializes to CSV
    """

    media_type = 'text/csv'
    format = 'csv'
    level_sep = '.'
    header = None
    labels = None  # {'<field>':'<label>'}
    writer_opts = None

    def render(self, data, media_type=None, renderer_context={}, writer_opts=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            return ''

        if not isinstance(data, list):
            data = [data]

        if writer_opts is not None:
            log.warning('The writer_opts argument is deprecated. Pass the '
                        'writer_opts attribute into renderer_context instead.')

        writer_opts = renderer_context.get('writer_opts', writer_opts or self.writer_opts or {})

        renderer_context = renderer_context or {}
        header = renderer_context.get('header', self.header)
        labels = renderer_context.get('labels', self.labels)

        table = self.tablize(data, header=header, labels=labels)
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer, **writer_opts)
        for row in table:
            # Assume that strings should be encoded as UTF-8
            csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in row
            ])

        return csv_buffer.getvalue()

    def tablize(self, data, header=None, labels=None):
        """
        Convert a list of data into a table.
        """
        if data:

            # First, flatten the data (i.e., convert it to a list of
            # dictionaries that are each exactly one level deep).  The key for
            # each item designates the name of the column that the item will
            # fall into.
            data = self.flatten_data(data)
            data.header = header or data.header

            # Get the set of all unique headers, and sort them (unless already provided).
            if not data.header:
                headers = set()
                for item in data:
                    headers.update(list(item.keys()))
                data.header = sorted(headers)

            # Create a row for each dictionary, filling in columns for which the
            # item has no data with None values.
            rows = []
            for item in data:
                row = []
                for key in data.header:
                    row.append(item.get(key, None))
                rows.append(row)

            # Return your "table", with the headers as the first row.
            if labels:
                return [[labels.get(x, x) for x in data.header]] + rows
            else:
                return [data.header] + rows

        else:
            return []

    def flatten_data(self, data):
        """
        Convert the given data collection to a list of dictionaries that are
        each exactly one level deep. The key for each value in the dictionaries
        designates the name of the column that the value will fall into.
        """
        flat_data = OrderedRows(data.header if hasattr(data, 'header') else None)
        for item in data:
            flat_item = self.flatten_item(item)
            flat_data.append(flat_item)

        return flat_data

    def flatten_item(self, item):
        if isinstance(item, list):
            flat_item = self.flatten_list(item)
        elif isinstance(item, dict):
            flat_item = self.flatten_dict(item)
        else:
            flat_item = {'': item}

        return flat_item

    def nest_flat_item(self, flat_item, prefix):
        """
        Given a "flat item" (a dictionary exactly one level deep), nest all of
        the column headers in a namespace designated by prefix.  For example:

         header... | with prefix... | becomes...
        -----------|----------------|----------------
         'lat'     | 'location'     | 'location.lat'
         ''        | '0'            | '0'
         'votes.1' | 'user'         | 'user.votes.1'

        """
        nested_item = {}
        for header, val in flat_item.items():
            nested_header = self.level_sep.join([prefix, header]) if header else prefix
            nested_item[nested_header] = val
        return nested_item

    def flatten_list(self, l):
        flat_list = {}
        for index, item in enumerate(l):
            index = text_type(index)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_item(flat_item, index)
            flat_list.update(nested_item)
        return flat_list

    def flatten_dict(self, d):
        flat_dict = {}
        for key, item in d.items():
            key = text_type(key)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_item(flat_item, key)
            flat_dict.update(nested_item)
        return flat_dict

    def headers():
        doc = ("The headers property. Kept around for backward compatibility."
               "Use the header attribute instead.")
        def fget(self):
            log.warning('The CSVRenderer.headers property is deprecated. '
                        'Use CSVRenderer.header instead.')
            return self.header
        def fset(self, value):
            log.warning('The CSVRenderer.headers property is deprecated. '
                        'Use CSVRenderer.header instead.')
            self.header = value
        def fdel(self):
            log.warning('The CSVRenderer.headers property is deprecated. '
                        'Use CSVRenderer.header instead.')
            del self.header
        return locals()
    headers = property(**headers())


class CSVRendererWithUnderscores (CSVRenderer):
    level_sep = '_'


class CSVStreamingRenderer(CSVRenderer):

    def render(self, data, media_type=None, renderer_context={}):
        """
        Renders serialized *data* into CSV to be used with Django
        StreamingHttpResponse. We need to return a generator here, so Django
        can iterate over it, rendering and returning each line.

        >>> renderer = CSVStreamingRenderer()
        >>> renderer.headers = ['a', 'b']
        >>> data = [{'a': 1, 'b': 2}]
        >>> from django.http import StreamingHttpResponse
        >>> response = StreamingHttpResponse(renderer.render(data),
                                             content_type='text/csv')
        >>> response['Content-Disposition'] = 'attachment; filename="f.csv"'
        >>> # return response

        """
        if data is None:
            yield ''

        self.labels = renderer_context.get('labels', self.labels)

        if not isinstance(data, list):
            data = [data]

        table = self.tablize(data)
        csv_buffer = Echo()
        csv_writer = csv.writer(csv_buffer)
        for row in table:
            # Assume that strings should be encoded as UTF-8
            yield csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in row
            ])
