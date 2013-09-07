#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aside_tree as ast

import sys

class TestDocument(ast.Document):
	def __init__(self):
		super(TestDocument,self).__init__()

	def _append(self, text, attributes):
		sys.stdout.write(text)

ast.document = TestDocument()

ast.root.render()

 
