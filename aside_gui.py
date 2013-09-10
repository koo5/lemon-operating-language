#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import sys

import aside_tree as ast

class CodeArea(ast.Document):

	def __init__(self, width, height, batch, parent):
		ast.Document.__init__(self)
		ast.document = self
        
		self.root = ast.root
		
		self.parent = parent
		self.batch = batch
		
		self.document = pyglet.text.document.FormattedDocument("ABC")
		self.document.set_style(0, len(self.document.text),
			dict(color=(255,255,255,255)))#, font_name="monospace")) #StopIteration
						
		self.layout = pyglet.text.layout.IncrementalTextLayout(
					self.document, width, height, multiline=True, batch=batch)

		ast.caret = self.caret = pyglet.text.caret.Caret(self.layout, self.batch, (255,0,0))
		
		self.active_caret = self.caret

		self.layout.x = 2
		self.layout.y = 2

		parent.push_handlers(self.on_text, self.on_key_press, self.on_mouse_press)

		self.rerender()

	def rerender(self):
		pos = self.caret.position
		self.document.text = ""
		self.root.render()
		self.caret.position = pos#restore

	def resize(self, width, height):
		self.layout.width = width
		self.layout.height = height

	def _append(self, text, attributes):
		self.document.insert_text(len(self.document.text),text, attributes)
		sys.stdout.write(text)

	
	def on(self, pos=None):
		if pos == None:
			pos = self.caret.position
		return self.document.get_style("element", pos)
	
	def on_text(self, text):
		self.on().on_text(text)
		self.rerender()

	def on_text_motion(self, motion):
		self.on().on_text_motion(motion)
		self.rerender()
		return pyglet.event.EVENT_UNHANDLED
	
	def on_text_motion_select(self, motion):
		self.on().on_text_motion_select(motion)
		self.rerender()
	
	def on_key_press(self, symbol, modifiers):
		self.on().on_key_press(symbol, modifiers)
		self.rerender()

	def on_mouse_press(self, x, y, button, modifiers):
		pos = self.layout.get_position_from_point(x,y)
		print "on_mouse_press", x, y, button, modifiers, pos
		self.on(pos).on_mouse_press(x, y, button, modifiers)
		self.rerender()
	

class Window(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(640, 400, caption='lemon is at it again',
				resizable=True)

		self.set_icon(pyglet.image.load('icon32x32.png'))


		self.batch = pyglet.graphics.Batch()
		self.code = CodeArea(self.width, self.height, self.batch, self)
		
		self.test()
		
	def on_resize(self, width, height):
		super(Window, self).on_resize(width, height)
		self.code.resize(width, height)

	def on_draw(self):
		pyglet.gl.glClearColor(0, 0, 0, 1)
		self.clear()
		self.batch.draw()
		
	def test(self):
		self.code.root.dump()
	#	pyglet.clock.schedule_interval(self.test_1, 5)
		pyglet.clock.schedule_interval(self.test_2, 2)
	
	def test_1(self, d):
		self.code.on_mouse_press(3,372,1,16)

	def test_2(self, d):
		print self.code.root.statements.items[2].statements
		self.code.root.statements.items[2].statements.toggle_expanded()
		self.code.rerender()
		
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




