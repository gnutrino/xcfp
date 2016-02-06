#/usr/bin/python3
import struct
from .properties import PropertyType

class XCFParseError(Exception):
    pass

class Parser():
    def __init__(self, file):
        self.file = file

    def read(self, size):
        buf = self.file.read(size)
        if len(buf) != size:
            raise IOError("Read Error")
        return buf

    def read_int(self):
        return struct.unpack("<i", self.read(4))[0]

    def read_str(self):
        size = self.read_int()
        bstr = self.read(size)

        #strings should be null terminated
        if bstr[-1] != 0:
            raise XCFParseError("Incorrect String size: {}".format(size))

        return bstr[:-1].decode("latin_1")

    def skip_padding(self):
        pad = self.read_int()
        if pad != 0:
            raise XCFParseError("Expected null padding DWORD, got {}".format(pad))

class PropertyParser(Parser):
    
    def properties(self):
        while True:
            prop = self.read_property()
            if prop is None:
                break
            yield prop

    def expect(self, name, typename):
        """read a property expecting it to have name 'name' and type
        'typename', if it doesn't throw an exception"""
        prop = self.read_property()

        if prop is None:
            raise XCFParseError("Expected Property {}:{} got None".format(name, typename))
        if prop.name != name or prop.typename != typename:
            raise XCFParseError("Expected Property {}:{}, got {}:{}".format(name, typename, prop.name, prop.typename))
        return prop

    def expect_none(self):
        if self.read_property() is not None:
            raise XCFParseError("Expected 'None' Property, got {}:{}".format(prop.name, prop.typename))

    def read_property(self):
        name = self.read_str()
        self.skip_padding()

        if name == 'None':
            return None

        typename = self.read_str()
        self.skip_padding()

        proptype = PropertyType(typename)

        size = self.read_int()
        self.skip_padding()

        data = proptype.read_data(self, size)
        return proptype(name).unpack(data)
