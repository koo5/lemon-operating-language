# -*- coding: utf-8 -*-

import pyglet

import element


class Widget(element.Element):
	pass

class Text(Widget):
	def __init__(self, text):
		super(Text, self).__init__()
		self.register_event_types('on_edit')
		self.push_handlers(
			on_text_motion = self.on_textwidget_text_motion,
			on_text = self.on_textwidget_text)
		document.push_handlers(
			post_render = self.post_render_move_caret)
		self.post_render_move_caret = 0
		self.color = (150,150,255,255)
		self.text = text
		
	def get_caret_position(self):
		"""
		if (document.caret.get_style("element") != self) and (document.caret.get_style("piece") != self) 
			return len(self.text)+1
		print "AA", document.caret.get_style("position")
		return document.caret.get_style("position")
		"""
		return document.caret.position - document.positions[self]

	def post_render_move_caret(self):
		if document.caret.get_style("element") != self:
			return

#		print "document.caret.position: ", document.caret.position
		
		m = self.post_render_move_caret
		self.post_render_move_caret = 0
		#move amount Node?:)

		if m == 0: return
#		print "move by: ", value

		if m < 0 and document.caret.position == 0:
			m = 0
		if m > 0 and document.caret.position == len(document.document.text):
			m = 0

		document.caret.position = document.caret.position + m
#		print self, "move by: ", value, " to ",document.caret.position
		
		
		
	def render(self):
		document.append(self.text, self)
	
	def on_textwidget_text(self, text):
		pos = self.get_caret_position()
		print "on_text pos: ", pos

		print self.text[:pos], text, self.text[pos:]
		self.text = self.text[:pos] + text + self.text[pos:]

		self.post_render_move_caret = len(text)

		#not wise to move the caret in the middle of rerendering

		#print self.text, len(self.text)
		self.dispatch_event('on_edit', self)
		return True

	
	def on_textwidget_text_motion(self, motion, select=False):
#		print "TextWidget on_text_motion"
		if motion == pyglet.window.key.MOTION_BACKSPACE:
			position = self.get_caret_position()
			if position > 0:
				self.text = self.text[:position-1]+self.text[position:]
			self.dispatch_event('on_edit', self)
			self.post_render_move_caret = -1
		else:
			return False

		print "returning True"
		return True


class ShadowedText(Text):

	def __init__(self, text, shadow):

		super(ShadowedText, self).__init__(text)
		self.shadow = shadow

	def render(self):

		document.append(self.text, self, {'color':self.color})
		document.append(self.shadow[len(self.text):], self, {'color':(130,130,130,255)})

	def len(self):
		return len(self.text+self.shadow[len(self.text)])
		


class Menu(Widget):
	def __init__(self, items):
		super(Menu, self).__init__()
		[self.register_event_type(i) for i in ['on_click']]
		self.color = (100,230,50,255)
		self.items = items
		self.sel = -1

	def render(self):
		for i, item in enumerate(self.items):
			#we will need to shift this here
			document.append("\n", self)
			document.append(item, self, 
				{'color':(255,100,100,255)} if self.sel == i else {})

		document.append("\n", self)
		
	




class Button(Widget):
	def __init__(self, text="[🔳]"):
		super(Button, self).__init__()
		self.register_event_types('on_click')
		self.color = (255,150,150,255)
		self.text = text
	def on_mouse_press(self, x, y, button, modifiers):
		#print "button clicked"
		self.dispatch_event('on_click', self)
	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.RETURN:
			print "button pressed"
			self.dispatch_event('on_click', self)
	def render(self):
		document.append(self.text, self)
	
class Number(Text):
	def __init__(self, text):
		super(Number, self).__init__(text)
		self.text = str(text)
		self.set('minus_button', Button("-"))
		self.set('plus_button', Button("+"))
		self.minus_button.push_handlers(on_click=self.on_widget_click)
		self.plus_button.push_handlers(on_click=self.on_widget_click)
	def render(self):
		self.minus_button.render()
		document.append(self.text, self)
		self.plus_button.render()
	@property
	def value(self):
		return int(self.text)
	def on_widget_click(self,widget):
		if widget == self.minus_button:
			self.text = str(int(self.text)-1)
		if widget == self.plus_button:
			self.text = str(int(self.text)+1)
			
class Toggle(Widget):
	def __init__(self, value):
		super(Toggle, self).__init__()
		self.value = value
	def render(self):
		document.append(self.text, self)
	@property
	def text(self):
		return "checked" if self.value else "unchecked"
	def on_mouse_press(self, x, y, button, modifiers):
		self.value = not self.value
		self.dispatch_event('on_edit')
		


