#!/usr/bin/python3

import unittest as ut
import os
import io
from xcfp.parser import Parser, XCFParseError

class TestParserRead(ut.TestCase):
    """Tests the Parser.read() method"""

    def setUp(self):
        self.data = b'\x01\x02\x03\x04\x05'
        self.parser = Parser(io.BytesIO(self.data))

    def test_read_full(self):
        self.assertEqual(self.parser.read(5), self.data)

    def test_read_parial(self):
        self.assertEqual(self.parser.read(4), self.data[:4])
        self.assertEqual(self.parser.read(0), b'')
        self.assertEqual(self.parser.read(1), self.data[4:])

    def test_read_beyond_EOF(self):
        with self.assertRaises(IOError):
            self.parser.read(6)

class TestParserReadInt(ut.TestCase):
    """Tests the Parser.read_int() method"""
    

    def test_read_int(self):
        test_cases = (
            #(data, expected)
            (b'\x00\x00\x00\x00', 0),
            (b'\x01\x00\x00\x00', 1),
            (b'\xff\xff\xff\xff', -1),
        )

        for data, expected in test_cases:
            with Parser(io.BytesIO(data)) as parser, self.subTest(i=expected):
                self.assertEqual(parser.read_int(), expected)

    def test_read_int_multiple(self):
        data = b'\x00\x00\x00\x00\x01\x00\x00\x00'
        with Parser(io.BytesIO(data)) as parser:
            self.assertEqual(parser.read_int(), 0, "First Read")
            self.assertEqual(parser.read_int(), 1, "Second Read")

class TestParserReadStr(ut.TestCase):
    """Tests the Parser.read_str() method"""

    def test_read_null(self):
        data = b'\x00\x00\x00\x00'
        with Parser(io.BytesIO(data)) as parser:
            self.assertEqual(parser.read_str(), '')

    def test_read_str(self):
        data = b'\x06\x00\x00\x00Hello\x00'
        with Parser(io.BytesIO(data)) as parser:
            self.assertEqual(parser.read_str(), 'Hello')

    def test_read_incorrect_size(self):
        data = b'\x04\x00\x00\x00Hello\x00'

        with Parser(io.BytesIO(data)) as parser, self.assertRaises(XCFParseError):
            parser.read_str()

    def test_read_str_multiple(self):
        data = b'\x06\x00\x00\x00Hello\x00\x07\x00\x00\x00World!\x00'

        with Parser(io.BytesIO(data)) as parser:
            self.assertEqual(parser.read_str(), 'Hello', "First Read")
            self.assertEqual(parser.read_str(), 'World!', "Second Read")

    def test_read_str_truncated(self):
        data = b'\x07\x00\x00\x00Hello\x00'

        with Parser(io.BytesIO(data)) as parser, self.assertRaises(IOError):
            parser.read_str()

from unittest import mock

@mock.patch.multiple('xcfp.parser', PropertyType=mock.DEFAULT, Property=mock.DEFAULT)
class TestPraserReadProperty(ut.TestCase):
    """Tests the Parser.read_property() method"""

    name_data1  = b'\x0d' + bytes(3) + b'strFirstName\x00' + bytes(4)
    type_data   = b'\x0c' + bytes(3) + b'StrProperty\x00' + bytes(4)
    size_data1  = b'\x08' + bytes(7)
    value_data1 = b'\x04' + bytes(3) + b'Ana\x00'
    data1 = name_data1 + type_data + size_data1 + value_data1

    name_data2  = b'\x0c' + bytes(3) + b'strLastName\x00' + bytes(4)
    size_data2  = b'\x0c' + bytes(7)
    value_data2 = b'\x08' + bytes(3) + b'Ramirez\x00'
    data2 = name_data2 + type_data + size_data2 + value_data2

    def setUpMocks(self, PropertyType, Property):
        mockPropType = mock.MagicMock(spec=('unpack',))
        mockPropType.typename = mock.sentinel.typename
        mockPropType.unpack.return_value = mock.sentinel.value
        PropertyType.return_value = mockPropType

        Property.return_value = mock.sentinel.Property

    def assert_calls(self, PropertyType, Property, name, typename, value):
        PropertyType.assert_called_with(typename)
        PropertyType.return_value.unpack.assert_called_with(value)
        Property.assert_called_with(name, mock.sentinel.typename, mock.sentinel.value)

    def test_read_property(self, PropertyType, Property):

        self.setUpMocks(PropertyType, Property)
        with Parser(io.BytesIO(self.data1)) as parser:
            self.assertIs(parser.read_property(), mock.sentinel.Property)
            self.assert_calls(PropertyType, Property, 'strFirstName', 'StrProperty', self.value_data1)

    def test_read_property_multiple(self, PropertyType, Property):

        self.setUpMocks(PropertyType, Property)

        with Parser(io.BytesIO(self.data1 + self.data2)) as parser:
            self.assertIs(parser.read_property(), mock.sentinel.Property, "First Call")
            self.assert_calls(PropertyType, Property, 'strFirstName', 'StrProperty', self.value_data1)

            self.assertIs(parser.read_property(), mock.sentinel.Property, "Second Call")
            self.assert_calls(PropertyType, Property, 'strLastName', 'StrProperty', self.value_data2)

class TestParserReadEmpty(ut.TestCase):
    """Tests the Parser reading an empty character pool (Empty.bin)"""

    def setUp(self):
        fname = os.path.join(os.path.dirname(__file__), 'Empty.bin')
        self.file = open(fname, 'rb')
        self.parser = Parser(self.file)

    def tearDown(self):
        self.file.close()

    def test_read_header(self):
        self.assertEqual(self.parser.read_header(), 0)

class TestParserReadFile(ut.TestCase):
    """Tests the Parser reading a sample valid file (Test1.bin)"""

    def setUp(self):
        fname = os.path.join(os.path.dirname(__file__), 'Test1.bin')
        self.file = open(fname, 'rb')
        self.parser = Parser(self.file)

    def tearDown(self):
        self.file.close()

    def test_read_header(self):
        self.assertEqual(self.parser.read_header(), 1)
