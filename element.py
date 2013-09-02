__author__ = 'ankhmorporkian'

import re

import pyglet

import lemon_logger
from lemon_exceptions import *
import marisa_trie


class Element(object):
    """Base element that all GUI elements derive from"""

    def __init__(self, parent=None, render=True, root=False, template=None):

        """
        Initialize element.
        :param parent: Parent, must be instance of Element if root is False, and will be None is root is True.
        :param render: Render the element or not?
        :param root: Root element on which other elements attach.

        """
        self.logger = lemon_logger.LemonLogger()
        self.__children = []
        self.render = render
        self.root = False
        self.template = template
        if (type(self) != Element) and root:  # Verify not a derived class if trying to assign as a root object.
            raise RootNotElement
        elif (not self.verifyElement(parent)) and (not root):  # Ensure parent is an object if not root
            raise InvalidElement
        elif root:
            self.__parent = None  # Root objects never have parents.
            self.root = True
        else:
            parent.addChild(self)
            self.__parent = parent  # No need to do cycle check yet as there are no children assigned.
            self.root = False

    def getChild(self, index):
        """
        Returns the child element at position index
        :param index: Position
        :return: :rtype: Element
        """
        return self.__children[index]

    def addChild(self, child):
        """
        Appends a child to end of element list.

        :param child: Element
        """
        if child.isRoot():
            raise RootNoParent
        elif not self.verifyElement(child):
            raise InvalidElement
        elif self.cycleSearch(child):
            raise CyclicElement
        else:
            self.__children.append(child)
            return True

    def delChild(self, child_to_delete):
        """
        Delete child matching child_to_delete
        :param child_to_delete: Child element to remove from list.
        :return: :rtype: :raise:
        """
        for index, child in enumerate(self.__children):
            if child_to_delete == child:
                self.__delChild(index)
                return True
        raise ElementNotFound

    def delChildTree(self, child_to_delete):
        """
        Delete child anywhere in entire tree, as opposed to first-level.
        :param child_to_delete: Child element to be deleted.
        :return: :rtype: :raise:
        """
        for index, child in enumerate(self.__children):
            if child == child_to_delete:
                self.__delChild(index)
                return True
            elif child.delChildTree(child_to_delete):
                return True
        raise ElementNotFound

    def getChildren(self):
        """
        Accessor for the list of child elements.

        :return: :rtype: list
        """
        return self.__children

    def getParent(self):
        """
        Accessor for __parent

        :return: :rtype: Element
        """
        return self.__parent

    def setParent(self, parent):

        """
        Private Method

        Reassign Element's parent to another parent. Must be of type element and much be consistent. Changes are not
        made until all sanity checks are completed.

        :param parent: Parent to reassign to. Will be checked to make sure there is not a cycle and is of type Element.
        :return: :rtype: Boolean
        """
        if self.root:  # Check if root element. If it is, refuse to assign a parent.
            raise RootNoParent

        if not isinstance(parent, Element):  # Make sure that the parent is derived from type Element.
            raise InvalidElement  # Maybe replace this with a parent specific exception?

        if self == parent:
            raise SelfNoParent  # Element may not be its own parent.

        if self.cycleSearch(parent):
            raise CyclicElement  # Element may not be its own ancestor.

        # At this point we can assume the change is valid. Perform the changes.
        try:
            self.__parent.delChild(self)
        except ElementNotFound:
            return False
        else:
            parent.addChild(self)
            self.__parent = parent  # TODO: There's probably a safer way to do this.

    def __setChildren(self, children):

        """
        Private accessor to overwrite list of children. Almost certainly a bad idea to use except to accomplish very
        specific goals.

        :param children: list of children to replace current list with.
        """
        self.__children = children

    def __insertChild(self, index, child):
        """
        Inserts a child element into the element list at specified index.

        :param index: Position to insert child into self.__children
        :param child: Child Element
        """
        self.__children.insert(index, child)

    def __delChild(self, index):
        """
        Private method to delete a child at specific index.
        :param index: Index
        :raise: IndexError
        """
        try:
            self.__children.pop(index)
        except IndexError:
            self.logger.critical("Index error in " + str(self) + ":delChild")
            raise IndexError

    def cycleSearch(self, new_parent):
        """Ensure that new_parent is not contained in the descendant tree in self.children"""

        return self.searchChildren(new_parent)

    def searchChildren(self, element):
        """Simple recursive check from membership."""
        for child in self.__children:
            if child == element or child.searchChildren(element):
                return True
        return False

    def verifyElement(self, element):
        """
        Simple check to make sure the passed option is instance of Element
        :param element: element to check
        :return: :rtype:
        """
        return isinstance(element, Element)

    def childCount(self):
        """
        Number of children in list, first-level.
        :return: :rtype:
        """
        return len(self.__children)

    def isRoot(self):
        """
        Check if current Element is root.

        :return: :rtype:
        """
        return self.root

    def returnRoot(self):
        """
        Return the root object.

        :return: :rtype:
        """
        if self.isRoot():
            return self
        current_object = self.__parent
        while not current_object.isRoot():  # TODO: Infinite loops should be impossible, but I want to verify that.
            current_object = current_object.getParent()
        return current_object

    def setPosition(self, column, row):
        """
        Set the position of the element, in character space.
        :param column:
        :param row:
        """
        self.column = column
        self.row = row
        for child in self.__children:
            child.setPosition(column, row)#...

    def draw(self, *args, **kwargs):
        offset = 0
        for x in self.getChildren():
            offset += x.getHeight() + 5
            x.draw(y=offset, *args, **kwargs)


            #def searchChildren(self, *args, **kwargs):
            #for x in self.getChildren():
            #    for y in args:
            #        if x.y:
            #            return x.y
            #    x.searchChildren()
            #return False

    def getHeight(self):
        pass

    def setTemplate(self, template):
        if not isinstance(template, Template):
            raise TypeError
        self.template = template

    def getTemplate(self):
        return self.template


class TextElement(Element):
    def __init__(self, parent, render=True, text='', font_name='monospace', font_size=12):
        super(TextElement, self).__init__(parent, render, False)
        self.__text = text
        self.logger.info('Set text in TextElement to: ' + self.__text)
        self.font = Font(font_name, font_size)
        self.label = pyglet.text.Label(' ',
                                       font_name=self.font.name,
                                       font_size=self.font.size,
                                       x=0, y=0)
        self.letter_width = self.label.content_width
        self.draw()

    def draw(self, x=0, y=0, y_flip=True, y_height=None, y_offset=0):
        #self.logger.info(y_height)
        self.x = x
        self.y = y - y_offset
        if y_flip and isinstance(y_height, int):
            y = y_height - self.y
        else:
            y = self.y
            #self.logger.info("X,Y,y_height",self.x,self.y,y_height,y_offset)
        self.label = pyglet.text.Label(self.__text,
                                       font_name=self.font.name,
                                       font_size=self.font.size,
                                       x=self.x, y=y)
        self.label.draw()

    def getX(self):
        return self.x

    def getY(self):
        return self.label.y

    def getHeight(self):
        return self.label.content_height

    def addText(self, letter, index=0):
        self.__text = letter.join([self.__text[:index], self.__text[index:]])

    def popText(self, index):
        if index < 0:
            return False
        else:
            self.__text = ''.join([self.__text[:index], self.__text[index + 1:]])
            return True


    def getWidth(self):
        return self.label.content_width

    def getLetterWidth(self):
        return self.letter_width

    def getLen(self):
        return len(self.__text)


class ButtonElement(Element):
    def __init__(self, parent, height=30, width=30):
        super(ButtonElement, self).__init__(parent=parent)
        self.height = height
        self.width = width

    def draw(self, y=100, x=100, y_offset=0, y_flip=True, y_height=None, *args, **kwargs):
        if y_flip and isinstance(y_height, int):
            y = y_height - y
        x1 = x
        y1 = y
        x2 = x + self.width
        y2 = y + 20
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

    def getHeight(self):
        return self.height


class Font(object):
    def __init__(self, name='monospace', size=12):
        self.name = name
        self.size = size


class Rectangle(object):
    def __init__(self, x1, y1, x2, y2):
        self.rectangle = pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))


class Template(object):
    def __init__(self, template_string, name=None):
        self.template_list = template_string.split()
        self.value_dict = dict()
        self.re = re.compile("<<(.*)>>")
        for idx, val in enumerate(self.template_list):
            if self.re.findall(val):
                self.template_list[idx] = self.re.findall(val)[0]
                self.value_dict[self.re.findall(val)[0]] = idx
        if name:
            self.name = name
        else:
            self.name = self.template_list[0]


    def setValue(self, key, value):
        if key in self.value_dict:
            self.template_list[self.value_dict[key]] = value
            return True
        else:
            return False

    def getValue(self, key):
        if key in self.value_dict:
            return self.template_list[self.value_dict[key]]

    def compileTemplate(self):
        return ' '.join(self.template_list)


class Value(object):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value


class TemplateManager(object):
    def __init__(self):
        self.templates = {}

    def addTemplate(self, template):
        if not isinstance(template, Template):
            raise TypeError
        self.templates[template.name] = template
        return len(self.templates)

    def getTemplate(self, name):
        return self.templates[name]

    def getTemplates(self):
        return self.templates

    def search(self, term):
        trie = marisa_trie.Trie([unicode(value) for value in self.templates.keys()])
        return self.templates[str(trie.keys(unicode(term))[0])]

    def searchAll(self, term):
        trie = marisa_trie.Trie([unicode(value) for value in self.templates.keys()])
        return [str(value) for value in trie.keys(unicode(term))]