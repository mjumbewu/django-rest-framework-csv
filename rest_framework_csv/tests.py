#-*- coding:utf-8 -*-
from StringIO import StringIO

from django.test import TestCase

from .renderers import CSVRenderer
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

        flat = renderer.tablize([{u'a': 1, u'b': u'hello\u2014goodbye'}])
        self.assertEqual(flat, [[u'a', u'b'            ],
                                [1   , u'hello—goodbye']])

    def test_render_a_list_with_unicode_elements(self):
        renderer = CSVRenderer()

        dump = renderer.render([{u'a': 1, u'b': u'hello\u2014goodbye', u'c': 'http://example.com/'}])
        self.assertEqual(dump, (u'a,b,c\r\n1,hello—goodbye,http://example.com/\r\n').encode('utf-8'))


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

        data = parser.parse(StringIO(csv_file), parser_context={'delimiter': ';'})

        self.assertEqual(data, [{'v1': 'a', 'v2': '1', 'v3': '2.3'},
                                {'v1': 'b', 'v2': '4', 'v3': '5.6'}])        
