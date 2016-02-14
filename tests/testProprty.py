#!/usr/bin/python3

import unittest as ut
from unittest.mock import sentinel
from xcfp.properties import Property

class TestPropertyConstructor(ut.TestCase):
    """Tests that the magic Property constructor works"""

    def test_property_constructor(self):
        class TestProperty(Property):
            typename = "TestProperty"
            expected_type = type(sentinel.value)

        prop = Property(sentinel.name, 'TestProperty', sentinel.value)
        self.assertIsInstance(prop, TestProperty)
        self.assertIs(prop.name, sentinel.name)
        self.assertIs(prop.value, sentinel.value)
