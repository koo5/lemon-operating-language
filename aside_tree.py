#!/usr/bin/env python
# -*- coding: utf-8 -*-



#lets ingraft this onto the element tree. get rid of the document parameters too?
#and fix all the naming conventions and formating and super() calls ...





"""
subclass from Document and implement append.
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
		self.on_a_new_line = True
	def __del__(self):
		#print self.text.replace("\n","\\n\n")
		print self.text
	def append(self, text, attributes):
		if self.on_a_new_line:
			self.on_a_new_line = False
			self.append(self.indentation*"    ",attributes)
		self.on_a_new_line = (text == "\n")
		self.text += text
		





class element(object):
	def on_text(self, motion):
		print self



"""

things that make up a template
indenting is still broken, as it is done with a newline...and sometimes newline comes before a dedent
"""

class piece(element):
	pass

class T(piece):
	def __init__(self, text):
		self.text = text
	def render(self, document, node):
		document.append(self.text, {"node":node})

class newline(piece):
	def render(self, document, node):
		document.append("\n" , {"node":node})#

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
widgets
"""
class widget(element):
	pass

#could we derive this from a label or something to save work?
#embed an unformateddocument and do something to a caret
class text_widget(widget):
	def __init__(self, text):
		self.inner_document = pyglet.UnformatedDocument(text)
		self.caret = pyglet.text.caret.Caret(self.layout, self.batch, (255,255,255))
	def render(self, document):
		document.append(self.inner_document.text, {"node":self})

	"""
	def on_text_motion(self, motion):
#		self.code.caret.on_text_motion(motion)
		print 

		
	def on_text_motion_select(self, motion):
		self.code.caret.on_text_motion_select(motion)

	def on_click(self):

	def grab_caret(self):
		document.active_caret = self.caret
	"""

class button_widget(widget):
	def __init__(self, text="[🔳]"):
		self.text = text
	def on_click(self):
		parent.clicked(self)
	def render(self, document):
		document.append(self.text, {"node":self})
	
class number_widget(widget):
	def __init__(self, text):
		self.text = text
		self.plus_button = button_widget()
		self.minus_button = button_widget()
	def render(self, document):
		self.minus_button.render(document)
		document.append(self.text, {"node":self})
		self.plus_button.render(document)
		
	






"""
the AST tree building blocks

in the end, it is always the node that is responsible for its render(), templated or not

some division of the boilerplatish AST rote from the gui handling stuff would be good

the AST stuff could be generated
"""


class ast_node(element):
	pass

class text_node(ast_node):
	def __init__(self, value):
		self.value = value
	def render(self, document):
		document.append(self.value, {"node":self})

class placeholder_node(ast_node):
	def __init__(self):#type..
		self.text = text_node("placeholder")
	def render(self, document):
		document.append("<<"+">>", {"node":self})
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...
	#def on_text(self, text):
	#	print "plap"

	

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
	def on_keypress(self, key, modifiers):
		if pyglet.MOD_CTRL in modifiers and key == pyglet.UP:
			prev_template()
		if pyglet.MOD_CTRL in modifiers and key == pyglet.DOWN:
			next_template()


class number_node(ast_node):
	def __init__(self, value):
		self.value = value
		self.minus_button = button_widget()
		self.plus_button = button_widget()
	def render(self, document):
		document.append(str(self.value), {"node":self})


#should this automatically indent? and show the button left of the first item...

class statements_node(ast_node):
	def __init__(self, items):
		self.items = items
		assert isinstance(items, list)
		self.expand_collapse_button = button_widget()
		self.set_expanded()
	def render(self, document):
		self.expand_collapse_button.render(document)
		newline().render(document, self)
		if not self.collapsed:
			for item in self.items:
				item.render(document)
				newline().render(document, self)
	def set_collapsed(self):
		self.collapsed = True
		self.expand_collapse_button.text = "+++"
	def set_expanded(self):
		self.collapsed = False
		self.expand_collapse_button.text = "---"




"""hummmmm, this is an odd one"""
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

 

"""


<AnkhMorporkian_> it's probably a bad idea to have newline as its own class. it'd be better to maintain it in the document class, since you have to have that anyways when you're using it.
<AnkhMorporkian> i understand why the nodes handle their own rendering, but I don't see why simple text characters should be.
<sirdancealot_> i wanted to have it uniform, to avoid special handling of str inside the template render


"""	
