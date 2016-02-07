#!/usr/bin/python
from collections import OrderedDict

from .properties import PropertyType, Property

class StructType(PropertyType):
    """Meta class for struct types"""

    structTypes = {}

    def __new__(cls, name, *args, **kwargs):

        #Allows StructProperty subclasses to be retrieved by structname as
        #StructType(str)
        if len(args) == 0:
            if name not in cls.structTypes:
                raise TypeError("Unknown Struct Type: {}".format(name))
            return cls.structTypes[name]

        (bases, namespace) = args
        #if we don't declare a structtype attribute we're in a base class that
        #should be hanled by the parent metaclass
        if 'structtype' not in namespace:
            return super().__new__(cls, name, *args, **kwargs)
        else:
            #otherwise we use type directly to create the structtype to stop it
            #going in knownTypes
            struct = type.__new__(cls, name, *args, **kwargs)
            cls.structTypes[struct.structtype] = struct
            return struct

class StructProperty(Property, metaclass=StructType):
    """Struct Property - a struct represented as a sequence of properties ended
    with 'None'"""

    typename = 'StructProperty'

    def unpack(self, data):
        from ..parser import Parser
        import io
        with Parser(io.BytesIO(data)) as parser:
            for prop in parser.properties():
                setattr(self, prop.name, prop)

        return self

    def __str__(self):
        return self.name

    @classmethod
    def data_read_hook(cls, parser, size):
        cls.structname = parser.read_str()
        parser.skip_padding()

        return size

class AppearanceStruct(StructProperty):
    """represents a TAppearance struct in a character file"""

    structtype = 'TAppearance'

    fields = OrderedDict((
        #(name, (type, defualt))
        #defaults taken from Ana Ramirez from the Demos&Replays.bin file that
        #comes with the game
        ('nmHead',  ('NameProperty', ('LatFem_C', 0))),
        ('iGender', ('IntProperty', 2)),
        ('iRace',   ('IntProperty', 3)),
    ))
