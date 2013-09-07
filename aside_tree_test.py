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


