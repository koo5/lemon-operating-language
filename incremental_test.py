#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet

import aside_tree as ast

class CodeArea(ast.Document):

	def __init__(self, width, height, batch):
		ast.Document.__init__(self)

		self.batch = batch
		
		self.document = pyglet.text.document.FormattedDocument("ABC")
		self.document.set_style(0, len(self.document.text),
								dict(color=(255, 255, 255, 255)))

		self.layout = pyglet.text.layout.IncrementalTextLayout(
					self.document, width, height, multiline=True, batch=batch)
					
		self.caret = pyglet.text.caret.Caret(self.layout)

		self.layout.x = 0
		self.layout.y = 0

	def resize(self, width, height):
		self.layout.width = width
		self.layout.height = height

	def append(self, text, attributes):
		self.document.insert_text(len(self.document.text),text, attributes)


class Window(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(640, 400, caption='lemon is at it again',
				resizable=True)

		self.batch = pyglet.graphics.Batch()
		self.code = CodeArea(self.width, self.height, self.batch)
		
		ast.root.render(self.code)


	def on_resize(self, width, height):
		super(Window, self).on_resize(width, height)
		self.code.resize(width, height)

	def on_draw(self):
#		pyglet.gl.glClearColor(0, 0, 0, 1)
		self.clear()
		self.batch.draw()
	"""
	def on_mouse_motion(
		self,
		x,
		y,
		dx,
		dy,
		):

		for widget in self.widgets:
			if widget.hit_test(x, y):
				self.set_mouse_cursor(self.text_cursor)
				break
		else:
			self.set_mouse_cursor(None)

	def on_mouse_press(
		self,
		x,
		y,
		button,
		modifiers,
		):

		for widget in self.widgets:
			if widget.hit_test(x, y):
				self.set_focus(widget)
				break
		else:
			self.set_focus(None)

		if self.focus:
			self.focus.caret.on_mouse_press(x, y, button, modifiers)

	def on_mouse_drag(
		self,
		x,
		y,
		dx,
		dy,
		buttons,
		modifiers,
		):

		if self.focus:
			self.focus.caret.on_mouse_drag(
				x,
				y,
				dx,
				dy,
				buttons,
				modifiers,
				)
	"""
	def on_text(self, text):
		self.code.caret.on_text(text)

	def on_text_motion(self, motion):
		self.code.caret.on_text_motion(motion)

	def on_text_motion_select(self, motion):
		self.code.caret.on_text_motion_select(motion)
	"""
	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.TAB:
			if modifiers & pyglet.window.key.MOD_SHIFT:
				direction = -1
			else:
				direction = 1

			if self.focus in self.widgets:
				i = self.widgets.index(self.focus)
			else:
				i = 0
				direction = 0

			self.set_focus(self.widgets[(i + direction)
						   % len(self.widgets)])
		elif symbol == pyglet.window.key.ESCAPE:

			pyglet.app.exit()

	def set_focus(self, focus):
		if self.focus:
			self.focus.caret.visible = False
			self.focus.caret.mark = self.focus.caret.position = 0

		self.focus = focus
		if self.focus:
			self.focus.caret.visible = True
			self.focus.caret.mark = 0
			self.focus.caret.position = len(self.focus.document.text)

	"""
window = Window(resizable=True)
pyglet.app.run()
