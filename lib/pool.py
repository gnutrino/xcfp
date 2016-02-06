from .character import Character
from .parser import PropertyParser, XCFParseError

class CharacterPool():
    
    def __init__(self, fname):
        self.fname = fname

    #context manager functions
    def __enter__(self):
        self.open() 
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self, fname=None):

        self.close()

        if fname is not None:
            self.fname = fname

        #if we can, open the file for reading and writing
        try:
            self.file = open(self.fname, 'a+b')
            self.file.seek(0)
            self.read_only = False
        except:
            #if that fails try to open it read only
            self.file = open(self.fname, 'rb')
            self.read_only = True

    def close(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def read_header(self):
        try:
            self.file.seek(0)
        except IOError:
            pass

        parser = PropertyParser(self.file)
        
        magic = parser.read_int()

        if magic != -1:
            raise XCFParseError("Incorrect Magic Number on file {}: {}".format(self.fname, magic))

        self.count = parser.expect('CharacterPool', 'ArrayProperty').value

        #I'm not actually convinced this is used, even if it is we're best
        #discarding it and recreating from the actual file name on write
        parser.expect('PoolFileName', 'StrProperty')

        parser.expect_none()

        count = parser.read_int()

        if count != self.count:
            raise XCFParseError("Mismatched character counts: {} != {}".format(count, self.count))

    def characters(self):
        """returns an iterator for the characters in this file"""

        self.read_header()

        parser = PropertyParser(self.file)

        for _ in range(self.count):
            char = Character()
            for prop in parser.properties():
                setattr(char, prop.name, prop)

            yield char
