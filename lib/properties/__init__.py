class PropertyError(Exception):
    pass

class PropertyType(type):
    """Meta class for properties"""

    knownTypes = {}

    def __new__(cls, name, *args, **kwargs):

        # Allows Proprty Types to be retrived by string name as ProprtyType(str)
        if len(args) == 0:
            if name not in cls.knownTypes:
                raise TypeError("Unknown PropertyType: {}".format(name))
            return cls.knownTypes[name]

        result = type.__new__(cls, name, *args, **kwargs)

        #lets us define abstract base classes that don't go into the KnowTypes
        #dict by leaving off the typename attribute
        if hasattr(result, 'typename'):
            cls.knownTypes[result.typename] = result

        return result

class Property(metaclass=PropertyType):
    """Base class for properties"""

    def __new__(cls, *args):

        #if we're in a subclass don't use special magic
        if cls != Property:
            return object.__new__(cls)

        #if called from the base class we find the actual type from the second
        #parameter and delegate to that class
        property_type = args[1]
        delegate_cls = PropertyType(property_type)
        return delegate_cls.__new__(delegate_cls, *args)

    def __init__(self, name, type=None, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value


    def unpack(self, data):
        self.value = self._unpack(data)
        return self

    @classmethod
    def _unpack(cls, data):
        raise NotImplementedError()

#make sure modules with Property subclasses get loaded whenever this package is
#used
from . import standard
from . import struct
