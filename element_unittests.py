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

    def test_template_add(self):
        template = Template('if <<a>> <<operator>> <<b>> then begin;\n<<stuff>>;\nend;')
        root = Element(root=True)
        self.assertEqual(root.getTemplate(), None)
        root.setTemplate(template)
        self.assertEqual(root.getTemplate().compileTemplate(), template.compileTemplate())


class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.root = Element(root=True)

    def test_if_set(self):
        template_string = "if <<first>> <<operator>> <<second>> then begin;"
        template = Template(template_string)
        template.setValue('first', '1')
        template.setValue('operator', '>')
        template.setValue('second', '0')
        self.assertEqual(template.getValue('first'), '1')
        self.assertEqual(template.getValue('second'), '0')
        self.assertEqual(template.getValue('operator'), '>')
        self.assertEqual(template.compileTemplate(), 'if 1 > 0 then begin;')

    def test_template_name(self):
        template_name = "test"
        template_string = "test <<a>> <<b>>"

        self.assertEqual(Template(template_string).name, Template('foobar', name=template_name).name)
        self.assertNotEqual(Template(template_string).name, Template('foobar').name)


class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.tm = TemplateManager()
        self.template = Template('test123 <<a>> <<b>>')

    def test_create(self):
        self.assertEqual(self.tm.getTemplates(), {})

    def test_add_template(self):
        self.assertEqual(self.tm.addTemplate(self.template), 1)
        self.assertEqual(self.tm.addTemplate(self.template), 1)  # Make sure that only one instance  is added.
        self.assertRaises(TypeError, self.tm.addTemplate, 'sup')  # Make sure you can only add a Template object.
        self.assertRaises(KeyError, self.tm.getTemplate, 'sup')
        self.assertEqual(self.tm.addTemplate(Template('boom', name='bam')), 2)

    def test_get_template(self):
        self.tm.addTemplate(self.template)
        self.assertEqual(self.tm.getTemplate('test123'), self.template)

    def test_template_search(self):
        self.tm.addTemplate(Template('if'))
        self.tm.addTemplate(Template('while'))
        self.tm.addTemplate(Template('when'))
        self.tm.addTemplate(Template('for'))
        self.tm.addTemplate(Template('define'))
        self.assertEqual(self.tm.search('i').name, Template('if').name)
        self.assertEqual(self.tm.search('wh').name, Template('when').name)
        self.assertEqual(self.tm.search('whi').name, Template('while').name)
        self.assertEqual(self.tm.search('f').name, Template('for').name)
        self.assertEqual(self.tm.search('d').name, Template('define').name)

    def test_search_all(self):
        self.tm.addTemplate(Template('if'))
        self.tm.addTemplate(Template('while'))
        self.tm.addTemplate(Template('when'))
        self.tm.addTemplate(Template('for'))
        self.tm.addTemplate(Template('define'))
        self.assertEqual(self.tm.searchAll('w'), ['when', 'while'])


if __name__ == '__main__':
    unittest.main()