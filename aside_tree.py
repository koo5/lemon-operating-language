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

def render_string(document, text, attributes):
	document.insert_text(len(document.text),text, attributes)

class newline(object):
	def render(self, document):
		document.append(document.indentation*"    " + "\n", {"node":self})#

class indent(object):
	def render(self, document):
		document.indent()

class dedent(object):
	def render(self, document):
		document.dedent()

class placeholder(object):
	def __init__(self, text):
	    self.text = text
	def render(self, document):
	    render_string(document, "<<"+self.text+">>", {"node":self})
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...






class template(object):
	def __init__(self, items):
	    self.items = items
	def render(self, document, node):
	    assert isinstance(document, Document)
	    for item in self.items:
	        if isinstance(item,str):
	            render_string(document, item, {"node":node})
	        else:
	            item.render(document)



			

        

        

class node(object):
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






	        
"""
a statements node needs a little more than a template
"""

class statements_node(node):
	def __init__(self, items):
		node.__init__(self)
		self.items = items
	def render(self, document):
		for item in self.items:
			item.render(document)
			newline().render(document)





class root_node(node):
	def __init__(self,statements, author="banana", date_created="1.1.1.1111"):
		node.__init__(self)
		self.templates = [template(["program by ",member("author"), indent(), newline(), member("nodes"), dedent()])]
		self.statements = statements
		self.author = text(author)
		self.date_created = text(date_created)

	def render(self, document):
		self.template.render(document, self)
		nodes.render(self, document)

class while_node(node):
	def __init__(self,condition,body):
		self.condition = condition
		self.body = body
		self.templates = [template(["while ", placeholder("condition"), " do:",newline(),indent(),placeholder("code to execute"),dedent()])]
		#,template([[0,"repeat if", placeholder("condition"), "is true:"],[1,placeholder("code to execute")],[0,"go back up.."]])]

class asignment_node(node):
	def __init__(self, name, value):
		node.__init__(self)
		self.name=name
		self.value = value
		self.templates=[template([placeholder("variable name"), " = ", placeholder("value")]),
									template(["set ", placeholder("variable name"), " to ", placeholder("value")]),
									template(["have ", placeholder("variable name"), " be ", placeholder("value")])]
									


newline().render(test_document())

template(["begin", " fun", newline(), "do stuff", newline(), "do stuff", newline(), "end"]).render(test_document(), "funs")

template([placeholder("thingy"), " 456"]).render(test_document(), "banana")


        
test = node()
test.templates = [template(["aaa"])]
test.render(test_document())



nodes([placeholder("aaa"), placeholder("bbb"), placeholder("ccc")]).render(test_document())


root = root_node([asignment_node("a", 0)]) 
#									while_node(is_less_than_node(variable_node("a"), constant_node(4)),
	#									nodes(print_node(variable_node("a"))))]



root.render(test_document())

root.items[0].prev_template()
root.render(test_document())
root.items[0].next_template()
root.render(test_document())
