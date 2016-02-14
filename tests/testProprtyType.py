#!/usr/bin/python3

import unittest as ut
from xcfp.properties import PropertyType, Property


class TestPropertyType(ut.TestCase):
    def test_propertytype(self):
        class TestProperty(Property):
            typename = 'TestProperty'
        self.assertIs(PropertyType('TestProperty'), TestProperty)

    def test_register_with_typename(self):
        class TestProperty():
            typename = 'TestProperty'
        PropertyType.register(TestProperty)
        self.assertIs(PropertyType('TestProperty'), TestProperty)

    def test_register_without_typename(self):
        class TestProperty():
            pass
        PropertyType.register(TestProperty, 'TestProperty')
        self.assertIs(PropertyType('TestProperty'), TestProperty)

    def test_deregister(self):
        class TestProperty(Property):
            typename = 'TestProperty'
        PropertyType.deregister(TestProperty)
        with self.assertRaises(TypeError):
            PropertyType('TestProperty')
