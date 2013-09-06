#!/usr/bin/env python
# -*- coding: utf-8 -*-



#lets ingraft this onto the element tree. get rid of the document parameters too?
#and fix all the naming conventions and formating and super() calls ...





"""
subclass from Document and implement append.
"""
document = test_document()
global document

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
		self.indent_length = 4

	def __del__(self):
		#print self.text.replace("\n","\\n\n")
		print self.text

	def append(self, text, attributes):
		if self.on_a_new_line:
			self.on_a_new_line = False
			self.append(self.return_indent(),attributes)
		self.on_a_new_line = (text == "\n")
		self.text += text

	def return_indent(self):
		return " "*self.indent_length
		





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
		
	


class Template(object):
	def __init__(self, string, dictionary={}):
		self.string = string
		self.dictionary = dictionary

	def render(self, data=None):
		if data:
			self.setData(data)

		document.append(self.string%self.dictionary)
	"""
		for item in self.chunks:
			if chunk is text: document.append(chunk, {"element":data?}
			if chunk is a key: document.data[key].render()...

	"""
		
	def setData(self,data):
		for key,value in data:
			try:
				self.dictionary[key] = value
			except IndexError:
				print "Couldn't assign %s:%s to Template!" % (idx,element)



def SimpleTemplate(istring,default_values):
        keyssearch = re.compile(r'.*?\%\((.*?)\)s')
#we need to parse out the inbetween texts too
        keys = keyssearch.findall(istring)
        output_dict = dict(zip(keys,default_values))
	not_keys = re.compile(r'(?!\(.*?\))')
	outlist = []
	tstring = istring
	for key in keys:
		outlist+=tstring.split(' %(%s) ')[0]
		outlist+=key

        class MetaTemplate(Template):
                string = istring
                dictionary = output_dict
		key_list = keys
                def __init__(self, data=None):
                        self.data = data or self.string
                        super(MetaTemplate,self).__init__(self.data, self.dictionary)
        return MetaTemplate

templates = {
'text' : SimpleTemplate("%(text)s", ('')) # Oh no they aren't global!
'placeholder' : SimpleTemplate("<<%(text)s>>", ('')),
'root' : SimpleTemplate("Program by %(author)s created on %(date)s, my whole code, indented:",('nobody', '1/1/2001')),
'while' : SimpleTemplate("while %(left_value)s %(operator)s %(right_value)s do:\n%(block)s",('a','==','b','\n')),
'if' : SimpleTemplate("if %(left_value)s %(operator)s %(right_value)s do:\n%(block)s",('a','==','b','\n')),
'assignment' : SimpleTemplate("%(left_value)s = %(right_value)s",('a','b')),
'print' : SimpleTemplate("print %(statement)s",(''))
}


"""
the AST tree building blocks

in the end, it is always the node that is responsible for its render(), templated or not

some division of the boilerplatish AST rote from the gui handling stuff would be good

the AST stuff could be generated
"""


class ast_node(element):
	def __init__(self,data,template):
		self.data = data
		self.template = template(data)

	def render(self,document):
		self.template.render()

	@property
	def keys(self):
		return self.template.keys	

	def setKey(self, key, value)
		try:
			self.data[key] = value
		except IndexError:
			print "Could not set data key %s to %s" % (key,value)

	def setTemplate(self, template, data=None):
		self.template = template(data)
		self.data = data

#	def __iadd__(self,value):  #Override later when the templating is cleaned up.
#		self.template_index += value
#		if value >0:
			

class text_node(ast_node):
	def __init__(self, data):
		super(text_node,self).__init__(data,templates['text']) # Add template later

class placeholder_node(text_node):
	def __init__(self):#type..
		super(placeholder_node,self).__init__(data,templates['placeholder'])

class number_node(ast_node):
	def __init__(self, data):
		super(number_node,self).__init__(data=data)
		self.minus_button = button_widget() #Should move these to the template later
		self.plus_button = button_widget()

	def render(self, document):
		document.append(str(self.data), {"node":self})


#should this automatically indent? and show the button left of the first item...

class statements_node(ast_node):
	def __init__(self, items):
		super(statements_node,self).__init__(data=items)
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
		super(variable_node,self).__init__()
		self.name = text_node(name) #Should move to a template later.
	def render(self, document):
		self.name.render(document)
		



"""
now onto real programming
"""


class root_node(ast_node):
	def __init__(self,data):
		super(root_node,self).__init__(data,templates['root'])
		
class while_node(ast_node):
	def __init__(self,data):
		super(while_node,self).__init__(data,templates['while'])

class assignment_node(ast_node):
	def __init__(self, data):
		super(assignment_node,self).__init__(data,templates['assignment'])
		
class print_node(ast_node):
	def __init__(self,data):
		super(print_node,self).__init__(data,templates['print'])









"""
x = text_template().render()
test = templated_node()
test.templates = [template([T("hello")])]
test.render(test_document())



root = root_node(statements_node([asignment_node(text_node("a"), number_node(1)),
																asignment_node(text_node("b"), number_node(5)), 
									while_node(is_less_than_node(variable_node("a"), variable_node("b")),
										statements_node([print_node(variable_node("a")), placeholder_node()])), placeholder_node()]))

root.render(test_document())
"""
 

"""


<AnkhMorporkian_> it's probably a bad idea to have newline as its own class. it'd be better to maintain it in the document class, since you have to have that anyways when you're using it.
<AnkhMorporkian> i understand why the nodes handle their own rendering, but I don't see why simple text characters should be.
<sirdancealot_> i wanted to have it uniform, to avoid special handling of str inside the template render


"""	
