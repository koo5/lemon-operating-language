#!/usr/bin/env python




"""

a bit of a mess here but this could correspond to a subclass of a formatted document or work in a similar fashion

"""

class Document(object):
	pass

class test_document(Document):
	def __init__(self):
		self.text = ""
		self.indentation = 0
	def insert_text(self, pos, text, attributes):
		self.text += text
	def __del__(self):
		#print self.text.replace("\n","\\n\n")
		print self.text
	def indent(self):
		self.indentation += 1
	def dedent(self):
		self.indentation -= 1
	def append(self, text, attributes):
		self.insert_text(len(self.text),text, attributes)







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
	pass


class placeholder_node(ast_node):
	def __init__(self):#type..
		pass
	def render(self, document):
		render_string(document, "<<"+self.text+">>", {"node":self})
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...

	

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


class statements_node(ast_node):
	def __init__(self, items):
		ast_node.__init__(self)
		self.items = items
	def render(self, document):
		for item in self.items:
			item.render(document)
			newline().render(document, self)







"""
now onto real programming
"""


class root_node(templated_node):
	def __init__(self,statements, author="banana", date_created="1.1.1.1111"):
		templated_node.__init__(self)
		self.templates = [template([T("program by "),child("author"), T(" created on "), child("date_created"), indent(), newline(), child("statements"), dedent(), T("end.")])]
		self.statements = statements
		self.author = text_node(author)
		self.date_created = text_node(date_created)

class while_node(templated_node):
	def __init__(self,condition,body):
		self.templates = [template([T("while "), child("condition"), T(" do:"),indent(), newline(),child("code to execute"),dedent()])]
		#,template([[0,"repeat if", child("condition"), "is true:"],[1,placeholder("code to execute")],[0,"go back up.."]])]
		self.condition = condition
		self.body = body

"""
class asignment_node(node):
	def __init__(self, name, value):
		node.__init__(self)
		self.name=name
		self.value = value
		self.templates=[template([placeholder("variable name"), " = ", placeholder("value")]),
									template(["set ", placeholder("variable name"), " to ", placeholder("value")]),
									template(["have ", placeholder("variable name"), " be ", placeholder("value")])]
"""									



	
test = templated_node()
test.templates = [template([T("aaa")])]
test.render(test_document())



#root = root_node([asignment_node("a", 0)]) 
#									while_node(is_less_than_node(variable_node("a"), constant_node(4)),
	#									nodes(print_node(variable_node("a"))))]

root = root_node(statements_node([text_node("banana"), text_node("banana"), text_node("lemon")]))

root.render(test_document())

 
