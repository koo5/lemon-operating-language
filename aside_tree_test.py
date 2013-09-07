#!/usr/bin/env python
# -*- coding: utf-8 -*-


import aside_tree as ast


class test_document(ast.Document):
	def __init__(self):
		super(test_document, self).__init__(self)
		self.text = ""
		self.on_a_new_line = True
		self.indent_length = 4

	#this no longer works with one global test_document
	#def __del__(self):
		#print self.text.replace("\n","\\n\n")
		#print self.text

	def append(self, text, attributes):
		if self.on_a_new_line:
			self.on_a_new_line = False
			self.append(self.return_indent(),attributes)
		self.on_a_new_line = (text == "\n")
		self.text += text
	#this should
		sys.stdout.write(text)
	
	def return_indent(self):
		return " "*self.indent_length
		



ast.document = test_document()


	
test = templated_node()
test.templates = [template([t("hello")])]
render.test()



root = root_node(statements_node([asignment_node(text_node("a"), number_node(1)),
																asignment_node(text_node("b"), number_node(5)), 
									while_node(is_less_than_node(variable_node("a"), variable_node("b")),
										statements_node([print_node(variable_node("a")), placeholder_node()])), placeholder_node()]))


root.render(test_document())

 
