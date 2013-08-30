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

    def test_find_element(self):
        root = Element(root=True)
        a = Element(root)
        c = Element(a)
        e = SubElement(c)

        self.assertTrue(a.searchChildren(c))
        self.assertTrue(a.searchChildren(e))
        self.assertTrue(c.searchChildren(e))

        self.assertFalse(a.searchChildren(a))

        b = Element(root)
        d = Element(b)
        f = Element(d)

        self.assertTrue(b.searchChildren(d))
        self.assertTrue(b.searchChildren(f))
        self.assertTrue(d.searchChildren(f))

        self.assertFalse(b.searchChildren(a))


if __name__ == '__main__':
    unittest.main()