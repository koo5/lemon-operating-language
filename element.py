__author__ = 'ankhmorporkian'

import lemon_logger
from lemon_exceptions import *


class Element(object):
    """Base element that all GUI elements derive from"""

    def __init__(self, parent=None, render=True, root=False):

        """
        Initialize element.
        :param parent: Parent, must be instance of Element if root is False, and will be None is root is True.
        :param render: Render the element or not?
        :param root: Root element on which other elements attach.

        """
        self.logger = lemon_logger.LemonLogger()
        self.__children = []
        self.render = render

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
        if child.root:
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
        for child in self.children:
            child.setPosition(column, row)#...

    def draw(self):
        """
        Perform rendering tasks for the element.
        """
        for child in self.children:
            child.draw()
