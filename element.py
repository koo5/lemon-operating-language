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

	def dump(self):
		document.append(self.__repr__(), self)
		for item in self.children.itervalues():
			document.indent()
			if isinstance(item, Element):
				item.dump()
			else:
				print item.__repr__()
			document.dedent()

	def on_text(self, text):
		print "on_text default:", self, text
		return False
	
	def on_text_motion(self, motion, select=False):
		print "on_text_motion default:", self, (
			pyglet.window.key.motion_string(motion),
			select)
		if motion == pyglet.window.key.MOTION_PREVIOUS_PAGE:
			print "pgup"
			for i in range(0,10):
				document.caret.on_text_motion(pyglet.window.key.MOTION_UP)
			return True

		elif motion == pyglet.window.key.MOTION_NEXT_PAGE:
			print "pgdn"
			for i in range(0,10):
				document.caret.on_text_motion(pyglet.window.key.MOTION_DOWN)
			return True

		else:
			print "passing to caret"
			document.caret.on_text_motion(motion, select)
			return True
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

