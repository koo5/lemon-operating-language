import element


class piece(element.Element):
	pass

class t(piece):
	def __init__(self, text):
		self.text = text
	def render(self, node, _=None):
		document.append(self.text, node)
class s(piece):
	def render(self, node, lastitem):
		document.append(" ", node.children[lastitem.name])
	
class newline(piece):
	def render(self, node, _=None):
		document.append("\n" , node)#

class indent(piece):
	def render(self, node, _=None):
		document.indent()

class dedent(piece):
	def render(self, node, _=None):
		document.dedent()

class child(piece):
	def __init__(self, name):
		self.name = name
	def render(self, node, _=None):
		node.children[self.name].render()
	




