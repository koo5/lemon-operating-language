__author__ = 'ankhmorporkian'
import unittest
import random

from element import *


class SubElement(Element):
    pass


class TestElement(unittest.TestCase):
    def setUp(self):
        self.root = Element(root=True)

    def test_add_element(self):
        for x in range(10):
            Element(self.root)
        self.assertEqual(len(self.root.getChildren()), 10)

    def test_add_improper_root(self):
        with self.assertRaises(RootNotElement):
            SubElement(root=True)

    def test_add_bad_parent(self):
        with self.assertRaises(InvalidElement):
            Element()

    def test_add_sub_elements(self):
        for element in self.root.getChildren():
            for x in range(random.randint(4, 9)):
                SubElement(element)


if __name__ == '__main__':
    unittest.main()