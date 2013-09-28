import pyglet

class Document(pyglet.event.EventDispatcher):
	"""
	subclass from Document,	implement append and....
	and set aside_tree.document to an instance of it
	"""
	def __init__(self):
		self.indentation = 0
		self.do_indent = True
		self.indent_length = 4
		#for kicking the cursor around:
		self.register_event_type('post_render')
		self.positions = {}
		self.active = None
		
	def indent(self):
		self.indentation += 1
	def dedent(self):
		self.indentation -= 1
			
	def append(self, text, element, attributes={}):
		if not self.positions.has_key(element):
			self.positions[element] = self.caret.position
		a = {'element':element, 'color':element.color}
		#update merges attributes into a
		a.update(attributes)
		#did we append a newline earlier?
		if self.do_indent:   
			self.do_indent = False
			self._append(self.indent_spaces(), a)
		self.do_indent = (text == "\n")
		self._append(text, a)
			
	def indent_spaces(self):
		return self.indent_length*" " * self.indentation
	def newline(self, element):
		self.append("\n", element)
	#lets get rid of using pieces.newline in the wrong places,
	#but doing newlines this explicitly might be useful later
	#even if only, or because, only known newlines, not inside
	#content ..but then again, nothing big..
