import nodes
import element
from pieces import *

import pyglet



class template(object):
	def __init__(self, items):
		self.items = items
	def render(self, node):
		#print self.items
		lastitem = None #im going to hell for this lastitem thing
		for item in self.items:
			assert(isinstance(item, piece))
			item.render(node, lastitem)
			lastitem = item






class Templated(nodes.Node):
	def __init__(self):
		super(Templated, self).__init__()
		self.template_index = 0
	@property
	def template(self):
		return self.templates[self.template_index]
	def render(self):
		self.template.render(self)
	def prev_template(self):
		self.template_index  -= 1
		if self.template_index < 0:
			self.template_index = 0
	def next_template(self):
		self.template_index  += 1
		if self.template_index == len(self.templates):
			self.template_index = len(self.templates)-1
	def on_key_press(self, key, modifiers):
		if (pyglet.window.key.MOD_CTRL & modifiers) and (key == pyglet.window.key.UP):
			self.prev_template()
			print("prev")
		if (pyglet.window.key.MOD_CTRL & modifiers) and (key == pyglet.window.key.DOWN):
			self.next_template()
			print("next")
