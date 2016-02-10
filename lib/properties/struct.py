#!/usr/bin/python
from collections import OrderedDict

from . import PropertyType, Property

class StructProperty(Property):
    """Struct Property - a struct represented as a sequence of properties ended
    with 'None'"""

    typename = 'StructProperty'

    def _get(self):
        return self

    def unpack(self, data):
        from ..parser import Parser
        import io
        with Parser(io.BytesIO(data)) as parser:
            for prop in parser.properties():
                setattr(self, prop.name, prop)

        return self

    def __str__(self):
        return "<struct: {}>".format(self.typename)

    @classmethod
    def data_read_hook(cls, parser, size):
        cls.typename = parser.read_str()
        parser.skip_padding()

        return size

class AppearanceStruct(StructProperty):
    """represents a TAppearance struct in a character file"""

    typename = 'TAppearance'

    fields = OrderedDict((
        #defaults taken from Ana Ramirez from the Demos&Replays.bin file that
        #comes with the game
        #(name,                 (type,                                  default))
        ('nmHead',              ('NameProperty',                ('LatFem_C', 0))),
        ('iGender',             ('IntProperty',                               2)),
        ('iRace',               ('IntProperty',                               3)),

        ('nmHaircut',           ('NameProperty',         ('Female_LongWavy', 0))),
        ('iHairColor',          ('IntProperty',                               0)),
        ('iFacialHair',         ('IntProperty',                               0)),
        ('nmBeard',             ('NameProperty',                    ('None', 0))),

        ('iSkinColor',          ('IntProperty',                               5)),
        ('iEyeColor',           ('IntProperty',                              15)),

        ('nmFlag',              ('NameProperty',          ('Country_Mexico', 0))),

        ('iVoice',              ('IntProperty',                              14)),
        ('iAttitude',           ('IntProperty',                               0)),

        ('iArmorDeco',          ('IntProperty',                              -1)),
        ('iArmorTint',          ('IntProperty',                              31)),
        ('iArmorTintSecondary', ('IntProperty',                              10)),
        ('iWeaponTint',         ('IntProperty',                              -1)),
        ('iTattooTint',         ('IntProperty',                              -1)),

        ('nmWeaponPattern',     ('NameProperty',             ('Pat_Nothing', 0))),

        ('nmPawn',              ('NameProperty',                    ('None', 0))),

        ('nmTorso',             ('NameProperty',          ('CnvMed_Std_C_F', 0))),
        ('nmArms',              ('NameProperty',          ('CnvMed_Std_F_F', 0))),
        ('nmLegs',              ('NameProperty',          ('CnvMed_Std_C_F', 0))),
        ('nmHelmet',            ('NameProperty',     ('Helmet_0_NoHelmet_F', 0))),
        ('nmEye',               ('NameProperty',             ('DefaultEyes', 3))),
        ('nmTeeth',             ('NameProperty',            ('DefaultTeeth', 0))),
        ('nmFacePropLower',     ('NameProperty',    ('Prop_FaceLower_Blank', 0))),

        ('nmPatterns',          ('NameProperty',             ('Pat_Nothing', 0))),

        ('nmVoice',             ('NameProperty', ('FemaleVoice1_English_US', 0))),
        ('nmLanguage',          ('NameProperty',                    ('None', 0))),

        ('nmTattoo_LeftArm',    ('NameProperty',       ('Tattoo_Arms_BLANK', 0))),
        ('nmTattoo_RightArm',   ('NameProperty',       ('Tattoo_Arms_BLANK', 0))),
        ('nmScars',             ('NameProperty',             ('Scars_BLANK', 0))),

        ('nmTorsoUnderlay',     ('NameProperty',     ('CnvUnderlay_std_A_F', 0))),
        ('nmArmsUnderlay',      ('NameProperty',     ('CnvMed_Underlay_A_F', 0))),
        ('nmLegsUnderlay',      ('NameProperty',     ('CnvUnderlay_std_A_F', 0))),
    ))
