#!/usr/bin/env python




"""

a bit of a mess here but this could correspond to a subclass of a formatted document or work in a similar fashion

"""

class Document(object):
	def __init__(self):
		self.indentation = 0
	def indent(self):
		self.indentation += 1
	def dedent(self):
		self.indentation -= 1

class test_document(Document):
	def __init__(self):
		Document.__init__(self)
		self.text = ""
	def _insert_text(self, pos, text, attributes):
		self.text += text
	def __del__(self):
		#print self.text.replace("\n","\\n\n")
		print self.text
	def append(self, text, attributes):
		self._insert_text(len(self.text),text, attributes)







"""

things that make up a template

"""

class piece(object):
	pass

class T(piece):
	def __init__(self, text):
		self.text = text
	def render(self, document, node):
		document.append(self.text, {"node":node})

class newline(piece):
	def render(self, document, node):
		document.append("\n"+document.indentation*"    " , {"node":node})#

class indent(piece):
	def render(self, document, node):
		document.indent()

class dedent(piece):
	def render(self, document, node):
		document.dedent()

class child(piece):
	def __init__(self, name):
		self.name = name
	def render(self, document, node):
		node.__dict__[self.name].render(document)
	








class template(object):
	def __init__(self, items):
		self.items = items
	def render(self, document, node):
		assert isinstance(document, Document)
		for item in self.items:
			assert(isinstance(item, piece))
			item.render(document, node)



			



"""
the AST tree building blocks
"""


class ast_node(object):
	def on_text(self, text):
		print "plop"

class placeholder_node(ast_node):
	def __init__(self):#type..
		pass
	def render(self, document):
		document.append("<<"+">>", {"node":self})
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...
	def on_text(self, text):
		print "plap"

	

class templated_node(ast_node):
	def __init__(self):
		self.template_index = 0
	template = property (lambda self: self.templates[self.template_index])
	def render(self, document):
		self.template.render(document, self)
	def prev_template(self):
		self.template_index  -= 1
		if self.template_index < 0:
			self.template_index = 0
	def next_template(self):
		self.template_index  += 1
		if self.template_index == len(self.templates):
			self.template_index = len(self.templates)-1


class text_node(ast_node):
	def __init__(self, value):
		self.value = value
	def render(self, document):
		document.append(self.value, {"node":self})

class number_node(ast_node):
	def __init__(self, value):
		self.value = value
	def render(self, document):
		document.append(str(self.value), {"node":self})

class statements_node(ast_node):
	def __init__(self, items):
		self.items = items
		assert isinstance(items, list)
	def render(self, document):
		for item in self.items:
			item.render(document)
			newline().render(document, self)




"""hummmmm"""
class variable_node(ast_node):
	def __init__(self, name):
		self.name = text_node(name)
	def render(self, document):
		self.name.render(document)
		







"""
now onto real programming
"""


class root_node(templated_node):
	def __init__(self,statements, author="banana", date_created="1.1.1.1111"):
		templated_node.__init__(self)
		self.templates = [template([T("program by "),child("author"), T(" created on "), child("date_created"), indent(), newline(), child("statements"), dedent(), T("end.")])]
		self.statements = statements
		assert isinstance(statements, statements_node)
		self.author = text_node(author)
		self.date_created = text_node(date_created)

class while_node(templated_node):
	def __init__(self,condition,body):
		templated_node.__init__(self)
		self.templates = [template([T("while "), child("condition"), T(" do:"),indent(), newline(),child("body"),dedent()]),
		template([T("repeat if"), child("condition"), T("is true:"),child("body"),T("go back up..")])]
		self.condition = condition
		self.body = body


class asignment_node(templated_node):
	def __init__(self, left, right):
		templated_node.__init__(self)
		self.left=left
		self.right=right
		self.templates=[template([child("left"), T(" = "), child("right")]),
									template([T("set "), child("left"), T(" to "), child("right")]),
									template([T("have "), child("left"), T(" be "), child("right")])]
		
class is_less_than_node(templated_node):
	def __init__(self, left, right):
		templated_node.__init__(self)
		self.left=left
		self.right=right
		self.templates=[template([child("left"), T(" < "), child("right")])]
		

class print_node(templated_node):
	def __init__(self,value):
		templated_node.__init__(self)
	
		self.templates = [template([T("print "), child("value")]),
									template([T("say"), child("value")])]
		self.value = value





	
test = templated_node()
test.templates = [template([T("hello")])]
test.render(test_document())



root = root_node(statements_node([asignment_node(text_node("a"), number_node(1)),
																asignment_node(text_node("b"), number_node(5)), 
									while_node(is_less_than_node(variable_node("a"), variable_node("b")),
										statements_node([print_node(variable_node("a")), placeholder_node()])), placeholder_node()]))


root.render(test_document())

 
