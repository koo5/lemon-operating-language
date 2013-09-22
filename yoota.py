#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet



class X(pyglet.event.EventDispatcher):
	def __init__(self):
		self.register_event_type('b')
		x = self.banana
		print id(self.banana)
		self.set_handler('b', self.banana)
		print id(self.banana)
		self.remove_handler('b', self.banana)
		print id(self.banana)
		self.dispatch_event('b')
		print id(self.banana)
		print x is self.banana

	def banana(self):
		print "WOOOOTA FUCKA"

x = X()

