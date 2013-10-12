import pyglet

class Element(pyglet.event.EventDispatcher):
	def __init__(self):
		super(Element,self).__init__()
		self.color = (200,255,200,255)
		self.children = {}
		self.parent = None
		self.register_event_types(
		'on_edit, on_text, on_text_motion, on_key_press, on_mouse_press')
	
	def __getattr__(self, name):

		if self.children.has_key(name):
			return self.children[name]
		else:
			raise AttributeError(name, self)

	def set(self, key, item):
		self.children[key] = item
		item.parent = self

	def replace(self, item):
		self.parent.children[
				self.parent.children.values.index(self)
			] = item

	def on_text(self, text):
		print "on_text default:", self, text
		return False
	
	def on_text_motion(self, motion, select=False):
		print "on_text_motion default:", self, (
			pyglet.window.key.motion_string(motion),
			select)
		return False

	def on_key_press(self, symbol, modifiers):
		print "on_key_press default:", self,(
			pyglet.window.key.modifiers_string(modifiers),
			pyglet.window.key.symbol_string(symbol))
		return False
		
	def on_mouse_press(self, x, y, button, modifiers):
		print "on_mouse_press default:", self, (
			x,y,button,modifiers)
		return False

	def is_caret_on_me(self):
		return active == self

	def register_event_types(self, types):
		for item in types.split(', '):
			self.register_event_type(item)

	def position(self):
		return self.doc.positions[self]
