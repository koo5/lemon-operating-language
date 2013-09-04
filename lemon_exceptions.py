#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'ankhmorporkian'


class InvalidElement(Exception):

    """Raised when object being inspected is not of type Element."""

    pass


class CyclicElement(Exception):

    """Raised when object would be its own ancestor."""

    pass


class RootNoParent(Exception):

    """
    Raised when trying to assign a root element a parent.
    Can probably be ignored in most cases, as root's parent
    will probably not be utilized.
    """

    pass


class SelfNoParent(CyclicElement):

    """
    Raised when trying to assign an element as its own parent.
    """


class RootNotElement(Exception):

    """
    Raised when trying to create an element as root when not of type Element.

    Derived classes may not be root.
    """

    pass


class ElementNotFound(Exception):

    """Element not found in search."""

    pass
