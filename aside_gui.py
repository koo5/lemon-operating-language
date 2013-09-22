#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import sys

import aside_tree as ast

class CodeArea(ast.Document):

	def __init__(self, width, height, batch, window):
		ast.Document.__init__(self)
		ast.document = self
        
		self.root = ast.root
		
		self.window = window
		self.batch = batch
		
		self.document = pyglet.text.document.FormattedDocument("ABC")
		#		self.document.set_style(0, len(self.document.text),
		#			dict(color=(255,255,255,255)))
		#				dict(color=(255,255,255,255), bold=False,italic=False,font_name="monospace", font_size=26)) 
		#http://code.google.com/p/pyglet/issues/list?can=1&q=stopiteration
						
		self.layout = pyglet.text.layout.IncrementalTextLayout(
					self.document, width-4, height-4, multiline=True, batch=batch)

		self.layout.x = 2
		self.layout.y = 2

		ast.caret = self.caret = pyglet.text.caret.Caret(self.layout, self.batch, (255,0,0))
		self.caret.position = 115

		window.set_handlers(self.on_text, self.on_text_motion, self.on_key_press, self.on_mouse_press)

		self.rerender()

	def rerender(self):
		ast.active = self.on()
		#we're gonna need it while rendering, and we're not gonna have it, 
		#because document.text is set to "" at the beginning
	
		print self.caret.position

		self.layout.begin_update()
		self.document.text = ""
		self.root.render()

#		self.document.set_style(0, len(self.document.text),
#			dict(bold=False,italic=False,font_name="monospace", font_size=26))
			
		self.layout.end_update()

		print self.caret.position

		self.dispatch_event('post_render')

		print self.caret.position

	def resize(self, width, height):
		self.layout.width = width
		self.layout.height = height

	def _append(self, text, attributes):
		self.document.insert_text(len(self.document.text),text, attributes)
#		sys.stdout.write(text)

	
	def on(self, pos=None):
		if pos == None:
			pos = self.caret.position
		print "pos: ",pos	
		return self.document.get_style("element", pos)
	
	def on_text(self, text):
		self.on().on_text(text)
		self.rerender()

	def on_text_motion(self, motion):
		print "ORANGE"
		
		res = self.on().on_text_motion(motion)
		self.rerender()
		return res
	
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
		super(Window, self).__init__(640, 400, caption='lemon party',
				resizable=True)

		self.set_icon(pyglet.image.load('icon32x32.png'))


		self.batch = pyglet.graphics.Batch()
		self.code = CodeArea(self.width, self.height, self.batch, self)
		
		self.test()
		
	def on_key_press(self, key, modifiers):
		if key == pyglet.window.key.F11:
			self.toggleFullscreen()
		else:
			return super(Window, self).on_key_press(key, modifiers)
		
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
	#	pyglet.clock.schedule_interval(self.test_2, 2)
	
	def test_1(self, d):
		self.code.on_mouse_press(3,372,1,16)

	def test_2(self, d):
		print self.code.root.statements.items[2].statements
		self.code.root.statements.items[2].statements.toggle_expanded()
		self.code.rerender()

	def toggleFullscreen(self):
		print "going fullscreen"
		self.set_fullscreen(not self.fullscreen)
		

	
window = Window()
pyglet.app.run()




