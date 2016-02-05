#!/usr/bin/python3
from struct import pack,unpack
from functools import partial
import io

class XCFParseError(Exception):
    pass


class XCFUnpacker(object):

    def __init__(self, file):
        self.f = file

    def unpack(self):
        chars = []
        magic = self._read_int()
        if magic != -1:
            raise XCFParseError("Incorrect Magic Number: {:x}".format(magic))

        self.count = self.read_property('CharacterPool', 'ArrayProperty').value

        self.fname = self.read_property('PoolFileName', 'StrProperty').value

        self.read_property('None')

        count = self._read_uint()
        if count != self.count:
            raise XCFParseError("Mismatched Character Counts: {} != {}".format(self.count, count))

        for _ in range(self.count):
            chars.append(self.parse_char())

        return chars

    def parse_char(self):
        """parse a character from file, returns a dictionary of XCFProperties
        representing the character"""
        char = []
        while True:
            prop = self.read_property()

            #'None' type properties represent the end of a character
            if prop.type == 'None':
                return char

            char.append(prop)


    def read_property(self, name=None, type=None):
        property_name = self._read_str()
        if name is not None and property_name != name:
            raise XCFParseError("Expecting property named {}, got {}".format(name, property_name))

        self._skip_padding()

        #sometimes we read a 'None' to indicate the end of things - return a
        #special 'None' property for this case to act as a sentinel
        if property_name == 'None':
            #print(('None'))
            return XCFProperty(None, 'None', None)

        property_type = self._read_str()
        if type is not None and property_type != type:
            raise XCFParseError("Expected property type {}, got {}".format(type, property_type))

        self._skip_padding()

        size = self._read_uint()

        self._skip_padding()

        #BoolProperties have size 0 but actually take 1 byte, I don't even
        #know...
        if property_type == 'BoolProperty' and size == 0:
            size = 1

        #for some reason Struct Properties have an extra string at the start
        #that isn't inluded in the size. For want of anything better to do with
        #it we just discard it
        if property_type == 'StructProperty':
            self._read_str()
            self._skip_padding()
            

        value = self._read(size)

        #print((property_name, property_type, value))
        return XCFProperty(property_name, property_type, value)

    def _read(self, n):
        buf = self.f.read(n)
        if len(buf) != n:
            XCFParseError("Unexpected EOF")
        return buf

    def _read_str(self):
        """read a string from the binary file 'file' where the first 4 bytes are
        the string length as a little endian unsigned int and the rest is the
        string. Assumes latin encoding."""
        size = self._read_uint()
        bstr = self._read(size)

        if bstr[-1] != 0:
            raise XCFParseError("Incorrect String Size: {}".format(size))

        return bstr[:-1].decode("latin_1")

    def _read_int(self):
        return unpack("<i", self._read(4))[0]

    def _read_uint(self):
        return unpack("<I", self._read(4))[0]

    def _skip_padding(self):
        pad = self._read_uint()
        if pad != 0:
            raise XCFParseError("Expected Padding DWord, got {}".format(pad))



class XCFProperty(object):
    def __init__(self, name, ptype, value):
        self.name = name
        self.type = ptype

        filters = {
            'ArrayProperty'  : self.unpack_int, #ArrayProperty.value is the length of the array
            'IntProperty'    : self.unpack_int,
            'BoolProperty'   : self.unpack_bool,
            'StrProperty'    : self.unpack_str,
            'NameProperty'   : self.unpack_name,
            'StructProperty' : self.unpack_struct,
            'None' : lambda _: None,
        }

        if self.type not in filters:
            raise XCFParseError("Unknown Property Type: {}".format(self.type))

        self.value = filters[self.type](value)

    def __str__(self):
        return str(self.value)


    def unpack_int(self, bstr):
        return unpack('<I', bstr)[0]

    def unpack_bool(self, bstr):
        return unpack('?', bstr)[0]

    def unpack_str(self, bstr):
        size = unpack('<I', bstr[:4])[0]
        if len(bstr[4:]) != size:
            raise XCFParseError("Incorrect String Size: {}".format(size))
        return bstr[4:-1].decode("latin_1")

    def unpack_name(self, bstr):
        #NameProperty has an extra DWord at the end, it's usually zero and
        #I don't know what it dows but we may as well return it
        name = self.unpack_str(bstr[:-4])
        val = self.unpack_int(bstr[-4:])
        return (name, val)

    def unpack_struct(self, bstr):
        #A bit hacky but as a struct has essentially the same format as a
        #character we'll just piggyback on XCFUnpacker.parse_char()
        unpacker = XCFUnpacker(io.BytesIO(bstr))
        return unpacker.parse_char()


if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        print("Usage: {} character_file".format(argv[0]))
        exit(1)

    with open(argv[1], "rb") as f:
        unpacker = XCFUnpacker(f)

        for char in unpacker.unpack():
            for prop in char:
                print("{}: {}".format(prop.name, prop.value))
            print('\n')
