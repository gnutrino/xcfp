from .properties import Property
from collections import OrderedDict

class Character():
    """Represents an XCOM 2 character in a character pool file"""

    # template for per instance field OrederedDicts
    _fields = OrderedDict((
        # name : (property_type, default)
        ('strFirstName', ('StrProperty', '')),
        ('strLastName',  ('StrProperty', '')),
        ('strNickName',  ('StrProperty', '')),

        ('m_SoldierClassTemplateName', ('NameProperty', ('Rookie', 0))),
        ('CharacterTemplateName',       ('NameProperty', ('Soldier', 0))),

        ('kAppearance', ('TAppearance', None)),

        ('Country', ('NameProperty', ('Country_UK', 0))),

        ('AllowedTypeSoldier', ('BoolProperty', True)),
        ('AllowedTypeVIP',     ('BoolProperty', True)),
        ('AllowedTypeDarkVIP', ('BoolProperty', True)),

        ('PoolTimestamp',  ('StrProperty', '')),
        ('BackgroundText', ('StrProperty', '')),
    ))

    def __init__(self):
        # keep an OrderedDict of the actual property objects for use when
        # writing out to file
        self.fields = OrderedDict()

        for name, args in self._fields.items():
            prop = Property(name, *args)
            self.fields[name] = prop
            setattr(self, name, prop)

    def __str__(self):
        fields = [str(x) for x in (self.strFirstName, self.strNickName, self.strLastName) if str(x)]

        return ' '.join(fields)

    def details(self):
        result = ""
        for name in self._fields.keys():
            result += "{}: {}\n".format(name, getattr(self, name))

        return result
