from .properties import PropertyType
from collections import OrderedDict

class Character():
    """Represents an XCOM 2 character in a character pool file"""
        
    Fields = OrderedDict((
        # name : (property_type, default)
        ('strFirstName', ('StrProperty', '')),
        ('strLastName',  ('StrProperty', '')),
        ('strNickName',  ('StrProperty', '')),

        ('m_SoldierClassTemplateName', ('NameProperty', ('Rookie', 0))),
        ('CharacterTemplateName',       ('NameProperty', ('Soldier', 0))),

        ('kAppearance', ('StructProperty', None)),

        ('Country', ('NameProperty', ('Country_UK', 0))),

        ('AllowedTypeSoldier', ('BoolProperty', True)),
        ('AllowedTypeVIP',     ('BoolProperty', True)),
        ('AllowedTypeDarkVIP', ('BoolProperty', True)),

        ('PoolTimestamp',  ('StrProperty', '')),
        ('BackgroundText', ('StrProperty', '')),
    ))

    def __init__(self):
        for name, (property_type, default) in self.Fields.items():
            setattr(self, name, PropertyType(property_type)(name, default))

    def __str__(self):
        fields = [str(x) for x in (self.strFirstName, self.strNickName, self.strLastName) if str(x)]

        return ' '.join(fields)

    def __setattr__(self, key, value):
        if key not in self.Fields:
            raise AttributeError("Tried to add an invalid field to Character: {}".format(key))

        super().__setattr__(key, value)

    def __getattr__(self, key):
        if key not in self.Fields:
            raise AttributeError("Tried to retrieve an invalid file from Character: {}".format(key))
        return super().__getattr__(key).value

    def details(self):
        result = ""
        for name in self.Fields.keys():
            result += "{}: {}\n".format(name, getattr(self, name))

        return result
