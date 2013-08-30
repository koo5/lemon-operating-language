__author__ = 'ankhmorporkian'

import lemon_logger
from lemon_exceptions import *


class Element(object):
    """Base element that all GUI elements derive from"""

    def __init__(self, parent=None, render=True, root=False):

        self.logger = lemon_logger.LemonLogger()
        self.children = []
        self.render = render

        if (type(self) != Element) and root:  # Verify not a derived class if trying to assign as a root object.
            raise RootNotElement

        if (not self.verifyElement(parent)) and (not root):  # Ensure parent is an object if not root
            raise InvalidElement
        elif root:
            self.__parent = None  # Root objects never have parents.
            self.root = True
        else:
            parent.addChild(self)
            self.__parent = parent  # No need to do cycle check yet as there are no children assigned.
            self.root = False

    def getChildren(self):
        return self.children

    def __setChildren(self, children):
        self.children = children

    def __setChild(self, index, child):
        try:
            self.children[index] = child
        except IndexError:
            self.logger.critical("Index error in " + str(self) + ":setChild")

    def addChild(self, child):
        if child.root:
            raise RootNoParent
        if not self.verifyElement(child):
            raise InvalidElement

    def getChild(self, index):
        try:
            return self.children[index]
        except IndexError:
            self.logger.critical("Index error in " + str(self) + ":getChild")

    def addChild(self, child):
        if self.cycleSearch(child):
            raise CyclicElement
        else:
            self.children.append(child)
            return True

    def __delChild(self, index):
        try:
            self.children.pop(index)
        except IndexError:
            self.logger.critical("Index error in " + str(self) + ":delChild")
            raise IndexError

    def delChild(self, child_to_delete):
        for index, child in enumerate(self.children):
            if child_to_delete == child:
                self.__delChild(index)
                return True
        raise ElementNotFound

    def delChildTree(self, child_to_delete):
        for index, child in enumerate(self.children):
            if child == child_to_delete:
                self.__delChild(index)
                return True
            elif child.delChildTree(child_to_delete):
                return True
        raise ElementNotFound

    def getParent(self):
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

    def cycleSearch(self, new_parent):
        """Ensure that new_parent is not contained in the descendant tree in self.children"""

        return self.searchChildren(new_parent)

    def verifyElement(self, element):
        return isinstance(element, Element)

    def searchChildren(self, element):
        """Simple recursive check from membership."""
        for child in self.children:
            if child == element or child.searchChildren(element):
                return True
        return False

    def isRoot(self):
        return self.root

    def returnRoot(self):
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
        for child in self.children:
            child.setPosition(column, row)#...

    def draw(self):
        """
        Perform rendering tasks for the element.
        """
        for child in self.children:
            child.draw()
