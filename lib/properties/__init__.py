#make sure modules with Property subclasses get loaded whenever this package is
#used
from . import properties
from . import struct

from .properties import PropertyType, Property
