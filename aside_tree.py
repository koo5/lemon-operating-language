#!/usr/bin/env python


#simulates a formated document + keeps track of indentation
class test_document(object):
	def __init__(self):
	    self.text = ""
	    self.indentation = 0
	def insert_text(self, pos, text, attributes):
	    self.text += text
	def __del__(self):
	    print self.text.replace("\n","\\n\n")
	def indent(self):
	    self.indentation += 1
	def dedent(self):
	    self.indentation -= 1
	def append(self, text, attributes):
	    self.insert_text(len(self.text),text, attributes)



def render_string(document, text, attributes):
	document.insert_text(len(document.text),text, attributes)


class newline(object):
	def render(self, document):
		document.append(document.indentation*"    " + "\n", {"node":self})#

		
newline().render(test_document(),{})

class template(object):
	def __init__(self, items):
	    self.items = items
	def render(self, document, node):
	    for item in self.items:
	        if isinstance(item,str):
	            render_string(document, item, {"node":node})
	        else:
	            item.render(document)
		newline().render({"node":node})


template(["begin", " fun", newline(), " do stuff", newline(), " do stuff", newline(), "end"]).render(test_document(), "funs")


			

class placeholder(object):
	def __init__(self, text):
	    self.text = text
	def render(self, document):
	    render_string(document, "<<"+self.text+">>", {"node":self})
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...

        

template([[0,placeholder("thingy"),"456"]]).render(test_document(), 0, "banana")

        

class node(object):
	def __init__(self):
		self.template_index = 0
	template = property (lambda self: self.templates[self.template_index])
	def render(self, document, indent):
		self.template.render(document, indent,self)
	def prev_template(self):
	    self.template_index  -= 1
	    if self.template_index < 0:
	        self.template_index = 0
	def next_template(self):
	    self.template_index  += 1
	    if self.template_index == len(self.templates):
	        self.template_index = len(self.templates)-1

	        
test = node()
test.templates = [template([[0,"aaa"]])]
test.render(test_document(), 2)

                        
		
class nodes(node):
	def __init__(self, items):
		node.__init__(self)
		self.items = items
	def render(self, document, indent):
		for item in self.items:
			item.render(document)
			newline().render(document)

nodes([placeholder("aaa"), placeholder("bbb"), placeholder("ccc")]).render(test_document(), 0)
			
class root_node(nodes):
	def __init__(self,items):
		nodes.__init__(self,items)
		self.templates = [template([[0, "program:"],[1, placeholder("nodes")]])]

	def render(self, document):
		self.template.render(self, document)
		nodes.render(self, document, 1)

class while_node(node):
	def __init__(self,condition,body):
		self.condition = condition
		self.body = body
		self.templates = [template([[0,"while", placeholder("condition"), "do:"],[1,placeholder("code to execute")]]),template([[0,"repeat if", placeholder("condition"), "is true:"],[1,placeholder("code to execute")],[0,"go back up.."]])]

class asignment_node(node):
	def __init__(self, name, value):
		node.__init__(self)
		self.name=name
		self.value = value
		self.templates=[template([[0, placeholder("variable name"), " = ", placeholder("value")]]),
									template([[0,"set ", placeholder("variable name"), " to ", placeholder("value")]]),
									template([[0, "have ", placeholder("variable name"), " be ", placeholder("value")]])]
									

root = root_node([asignment_node("a", 0)]) 
#									while_node(is_less_than_node(variable_node("a"), constant_node(4)),
	#									nodes(print_node(variable_node("a"))))]



root.render(test_document())

root.items[0].prev_template()
root.render(test_document(), 0)
root.items[0].next_template()
root.render(test_document(), 0)
