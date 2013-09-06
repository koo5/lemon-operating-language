#!/usr/bin/env python
# -*- coding: utf-8 -*-


import aside_tree as ast





for key, item in ast.templates.iteritems():
	print key
	item().render()
