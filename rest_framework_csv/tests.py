#-*- coding:utf-8 -*-
from __future__ import unicode_literals

import csv
from six import StringIO, PY3
from types import GeneratorType

from django.test import TestCase

from .renderers import CSVRenderer, CSVStreamingRenderer
from .parsers import CSVParser



class TestCSVRenderer (TestCase):

    def test_tablize_a_list_with_no_elements(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([])
        self.assertEqual(flat, [])

    def test_tablize_a_list_with_atomic_elements(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([1, 2, 'hello'])
        self.assertEqual(flat, [[''     ],
                                [1      ],
                                [2      ],
                                ['hello']])


    def test_tablize_a_list_with_list_elements(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([[1, 2, 3],
                                 [4, 5],
                                 [6, 7, [8, 9]]])
        self.assertEqual(flat, [['0' , '1' , '2'  , '2.0' , '2.1'],
                                [1   , 2   , 3    , None  , None ],
                                [4   , 5   , None , None  , None ],
                                [6   , 7   , None , 8     , 9    ]])

    def test_tablize_a_list_with_dictionary_elements(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([{'a': 1, 'b': 2},
                                 {'b': 3, 'c': {'x': 4, 'y': 5}}])
        self.assertEqual(flat, [['a' , 'b' , 'c.x' , 'c.y' ],
                                [1   , 2   , None  , None  ],
                                [None, 3   , 4     , 5     ]])

    def test_tablize_a_list_with_mixed_elements(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([{'a': 1, 'b': 2},
                                 {'b': 3, 'c': [4, 5]},
                                 6])
        self.assertEqual(flat, [[''  , 'a' , 'b' , 'c.0' , 'c.1'],
                                [None, 1   , 2   , None  , None ],
                                [None, None, 3   , 4     , 5    ],
                                [6   , None, None, None  , None ]])

    def test_tablize_a_list_with_unicode_elements(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([{'a': 1, 'b': 'hello\u2014goodbye'}])
        self.assertEqual(flat, [['a', 'b'            ],
                                [1   , 'hello—goodbye']])

    def test_tablize_with_labels(self):
        renderer = CSVRenderer()

        flat = renderer.tablize([{'a': 1, 'b': 2},
                                 {'b': 3, 'c': [4, 5]},
                                 6],
                                labels={'a':'A', 'c.0': '0c'})
        self.assertEqual(flat, [[''  , 'A' , 'b' , '0c' , 'c.1'],
                                [None, 1   , 2   , None  , None ],
                                [None, None, 3   , 4     , 5    ],
                                [6   , None, None, None  , None ]])

    def test_render_a_list_with_unicode_elements(self):
        renderer = CSVRenderer()

        dump = renderer.render([{'a': 1, 'b': 'hello\u2014goodbye', 'c': 'http://example.com/'}])
        if PY3:
            dump = dump.encode('utf-8')
        self.assertEqual(dump, ('a,b,c\r\n1,hello—goodbye,http://example.com/\r\n').encode('utf-8'))

    def test_render_ordered_rows(self):
        parser = CSVParser()
        csv_file = 'v1,v2,v3\r\na,1,2.3\r\nb,4,5.6\r\n'
        data = parser.parse(StringIO(csv_file))
        renderer = CSVRenderer()

        dump = renderer.render(data)
        self.assertEqual(dump, csv_file)  # field order should be maintained

        dump = renderer.render(data, renderer_context={'header': ['v3', 'v1', 'v2']})
        self.assertTrue(dump.startswith('v3,v1,v2\r\n'),  # field order should be overrideable
                        'Failed to override the header. Should be "v3,v1,v2". '
                        'Was {}'.format(dump.split()[0]))

    def test_render_subset_of_fields(self):
        renderer = CSVRenderer()
        renderer.header = ['a', 'c.x']

        data = [{'a': 1, 'b': 2},
                {'b': 3, 'c': {'x': 4, 'y': 5}}]
        dump = renderer.render(data)
        self.assertEqual(dump, 'a,c.x\r\n'
                               '1,\r\n,'
                               '4\r\n')

    def test_dynamic_render_subset_of_fields_with_labels(self):
        renderer = CSVRenderer()

        data = [{'a': 1, 'b': 2},
                {'b': 3, 'c': {'x': 4, 'y': 5}}]
        dump = renderer.render(data, renderer_context={'header': ['a', 'c.x'], 'labels': {'c.x':'x'}})
        self.assertEqual(dump, 'a,x\r\n'
                               '1,\r\n,'
                               '4\r\n')

    def test_render_data_with_writer_opts(self):
        renderer = CSVRenderer()
        renderer.header = ['a', 'b']
        data = [{'a': 'test', 'b': 'hello'}, {'a': 'foo', 'b': 'bar'}]
        writer_opts = {
            'quoting': csv.QUOTE_ALL,
            'quotechar': '|' if PY3 else b'|',
            'delimiter': ';' if PY3 else b';',
        }
        dump = renderer.render(data, writer_opts=writer_opts)
        self.assertEquals(dump.count(';'), 3)
        self.assertIn("|test|", dump)
        self.assertIn("|hello|", dump)

    def test_render_data_with_writer_opts_set_via_CSVRenderer(self):
        renderer = CSVRenderer()
        renderer.headers = ['a', 'b']
        data = [{'a': 'test', 'b': 'hello'}, {'a': 'foo', 'b': 'bar'}]
        writer_opts = {
            'quoting': csv.QUOTE_ALL,
            'quotechar': '|' if PY3 else b'|',
            'delimiter': ';' if PY3 else b';',
        }
        renderer.writer_opts = writer_opts
        dump = renderer.render(data)
        self.assertEquals(dump.count(';'), 3)
        self.assertIn("|test|", dump)
        self.assertIn("|hello|", dump)

    def test_render_data_with_writer_opts_set_via_renderer_context(self):
        renderer = CSVRenderer()
        renderer.headers = ['a', 'b']
        data = [{'a': 'test', 'b': 'hello'}, {'a': 'foo', 'b': 'bar'}]
        writer_opts = {
            'quoting': csv.QUOTE_ALL,
            'quotechar': '|' if PY3 else b'|',
            'delimiter': ';' if PY3 else b';',
        }
        dump = renderer.render(data, renderer_context={'writer_opts': writer_opts})
        self.assertEquals(dump.count(';'), 3)
        self.assertIn("|test|", dump)
        self.assertIn("|hello|", dump)


class TestCSVStreamingRenderer(TestCase):

    def setUp(self):
        self.header = ['a', 'b']
        self.data = [{'a': 1, 'b': 2}]

    def test_renderer_return_type(self):
        renderer = CSVStreamingRenderer()
        renderer.header = self.header
        dump = renderer.render(self.data)
        self.assertIsInstance(dump, GeneratorType)

    def test_renderer_value(self):
        renderer = CSVRenderer()
        renderer.header = self.header

        streaming_renderer = CSVStreamingRenderer()
        streaming_renderer.header = self.header

        renderer_data = renderer.render(self.data)
        streaming_renderer_data = ''.join(streaming_renderer.render(self.data))
        self.assertEqual(renderer_data, streaming_renderer_data)


class TestCSVParser(TestCase):

    def test_parse_two_lines_flat_csv(self):
        parser = CSVParser()
        csv_file = 'v1,v2,v3\r\na,1,2.3\r\nb,4,5.6\r\n'

        data = parser.parse(StringIO(csv_file))

        self.assertEqual(data, [{'v1': 'a', 'v2': '1', 'v3': '2.3'},
                                {'v1': 'b', 'v2': '4', 'v3': '5.6'}])

    def test_semi_colon_delimiter(self):
        parser = CSVParser()
        csv_file = 'v1;v2;v3\r\na;1;2.3\r\nb;4;5.6\r\n'

        delimiter = ';' if PY3 else b';'
        data = parser.parse(StringIO(csv_file), parser_context={'delimiter': delimiter})

        self.assertEqual(data, [{'v1': 'a', 'v2': '1', 'v3': '2.3'},
                                {'v1': 'b', 'v2': '4', 'v3': '5.6'}])

    def test_parse_stream_with_only_carriage_returns(self):
        parser = CSVParser()
        csv_file = 'Name,ID,Country\rKathryn Miller,67,United States\rJen Mark,78,Canada'

        data = parser.parse(StringIO(csv_file))
        self.assertEqual(data, [{'Name': 'Kathryn Miller', 'ID': '67', 'Country': 'United States'},
                                {'Name': 'Jen Mark',       'ID': '78', 'Country': 'Canada'}])

    def test_parse_file_with_only_carriage_returns(self):
        import os.path
        CURDIR = os.path.dirname(__file__)
        CSVFILE = os.path.join(CURDIR, 'testfixtures', 'nonewlines.csv')

        parser = CSVParser()

        with open(CSVFILE, 'rU') as csv_file:
            data = parser.parse(csv_file)
            self.assertEqual(data, [{'Name': 'Kathryn Miller', 'ID': '67', 'Country': 'United States'},
                                    {'Name': 'Jen Mark',       'ID': '78', 'Country': 'Canada'}])

    def test_unicode_parsing(self):
        parser = CSVParser()
        csv_file = 'col1,col2\r\nhello—goodbye,here—there'

        data = parser.parse(StringIO(csv_file))
        self.assertEqual(data, [{'col1': 'hello—goodbye', 'col2': 'here—there'}])
