#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, 'pyglet')

import pyglet

import aside_tree as ast

class CodeArea(ast.Document):

	def __init__(self, width, height, batch, window):
		ast.Document.__init__(self)
		ast.document = self
        
		ast.populate_root()
		
		self.window = window
		self.batch = batch
		
		#todo: switch to formatted_from_text, implement functions 
		#dealing with the text if necessary
		
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

		window.set_handlers(self.on_text, self.on_text_motion, self.on_key_press, self.on_mouse_press, self.caret.on_activate, self.caret.on_deactivate)

		self.rerender()

	def rerender(self):
		self.do_indent = True
		ast.active = self.on()
		#we're gonna need it while rendering, and we're not gonna have it, 
		#because document.text is set to "" at the beginning
	
		line = self.caret.line
		self.layout.begin_update()
		self.document.text = ""
		ast.root.render()
		self.document.set_style(0, len(self.document.text),
			dict(bold=False,italic=False,font_name="monospace", font_size=ast.root.startup_setting_font_size.value))
		self.layout.end_update()
		self.caret.line = min(line, self.layout.get_line_count()-1)
		self.dispatch_event('post_render')

	def resize(self, width, height):
		self.layout.width = width
		self.layout.height = height

	def _append(self, text, attributes):
		self.document.insert_text(len(self.document.text),text, attributes)
#		sys.stdout.write(text)

	
	def on(self, pos=None):
		if pos == None:
			pos = self.caret.position
#		print "pos: ",pos	
		return self.document.get_style("element", pos)
	
	def on_text(self, text):
		self.on().dispatch_event('on_text', text)
		self.rerender()

	def on_text_motion(self, motion):
		self.on().dispatch_event('on_text_motion', motion)
		self.rerender()
	
	def on_key_press(self, symbol, modifiers):
		self.on().dispatch_event('on_key_press', symbol, modifiers)
		self.rerender()

	def on_mouse_press(self, x, y, button, modifiers):
		pos = self.layout.get_position_from_point(x,y)
		self.on(pos).dispatch_event('on_mouse_press', x, y, button, modifiers)
		self.rerender()
		
	

class Window(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(440, 400, caption='lemon party',
				resizable=True)

		self.set_icon(pyglet.image.load('icon32x32.png'))

		self.batch = pyglet.graphics.Batch()
		self.code = CodeArea(self.width, self.height, self.batch, self)
		
	def toggleFullscreen(self):
		print "going fullscreen"
		self.set_fullscreen(not self.fullscreen)

	def on_key_press(self, key, modifiers):
		if key == pyglet.window.key.F11:
			self.toggleFullscreen()
			return True
		else:
			return super(Window, self).on_key_press(key, modifiers)
		
	def on_resize(self, width, height):
		super(Window, self).on_resize(width, height)
		self.code.resize(width, height)

	def on_draw(self):
		pyglet.gl.glClearColor(0, 0.1, 0.2, 1)
		self.clear()
		self.batch.draw()
		
		

	
window = Window()
pyglet.app.run()


