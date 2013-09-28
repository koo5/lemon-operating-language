#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

import sys
sys.path.insert(0, 'pyglet')
import pyglet

import document
import aside
from aside import *
import settings

def test_stuff():
	return Dict((
			"settings", Dict(
				("font_size", settings.FontSize()),
				("fullscreen", settings.Fullscreen())
				)
			),(
			"programs", List([
				Program(Statements([
					Placeholder(), 
					Asignment(Text("a"), Number(1)),
					Asignment(Text("b"), Number(5)), 
					While(IsLessThan(VariableRead("a"), VariableRead("b")),	Statements([
						Print(
							VariableRead("a")), #byname
							Placeholder()])),
					Placeholder()]), name="test1")])
			),(
			"notes", List([
				Todo("start looking into voice recognition (samson?)"),
				Todo("procrastinate more"),
				CollapsibleText(
					"""


<AnkhMorporkian_> it's probably a bad idea to have newline as its own class. it'd be better to maintain it in the document class, since you have to have that anyways when you're using it.
<AnkhMorporkian> i understand why the nodes handle their own rendering, but I don't see why simple text characters should be.
<sirdancealot_> i wanted to have it uniform, to avoid special handling of str inside the template render



					"""),

				CollapsibleText(
					"""
#couple options:
	store the positions of characters in an array ourselves - 
		hmm, this actually sounds pretty simple, might be dumping pyglets documents one day
	store positions in attributes char by char
		for everything
		for just active.. nope...clicks...
	settled for one position for each element now
					"""),
				Idea("""pick up the templating work, use an existing templating library, switch to formatted_from_text, implement functions dealing with the text with attributes if necessary"""),
				Todo("save/load nodes", priority=10),
				Todo("salvage the logger thingy...printing does get tedious...but its so damn quick")
				])
			),(
			"clock",Clock()
			)	
			)


class CodeArea(document.Document):

	def __init__(self, width, height, batch, window):
		document.Document.__init__(self)
		aside.set_document(self)
		
		self.root = test_stuff()
		#self.root.settings.fullscreen.push_handlers(on_change = self.on_settings_change)
		
		self.window = window
		self.batch = batch
		
		self.document = pyglet.text.document.FormattedDocument("")
		self.layout = pyglet.text.layout.IncrementalTextLayout(
					self.document, width-4, height-4, multiline=True, batch=batch)

		self.layout.x = 2
		self.layout.y = 2

		self.caret = pyglet.text.caret.Caret(self.layout, self.batch, (255,0,0))
		self.caret.position = 115

		window.set_handlers(self.on_text, self.on_text_motion, self.on_key_press, self.on_mouse_press, self.caret.on_activate, self.caret.on_deactivate)

		self.rerender()

	def on_settings_change(self, setting):
		if setting == self.root.settings.fullscreen:
			window.set_fullscreen(self.root.settings.fullscreen.value)

	def rerender(self):
		self.do_indent = True
		self.active = self.on()
		#we're gonna need it while rendering, and we're not gonna have it, 
		#because document.text is set to "" at the beginning
	
		line = self.caret.line
		self.layout.begin_update()
		self.document.text = ""
		self.root.render()
		self.document.set_style(0, len(self.document.text),
			dict(bold=False,italic=False,font_name="monospace",
			font_size=self.root.settings.font_size.value))
		self.layout.end_update()
		self.caret.line = min(line, self.layout.get_line_count()-1)
		self.dispatch_event('post_render')

	def resize(self, width, height):
		self.layout.width = width
		self.layout.height = height

	def _append(self, text, attributes):
		self.document.insert_text(len(self.document.text), text, attributes)
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


