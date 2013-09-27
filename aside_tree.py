#!/usr/bin/env python
# -*- coding: utf-8 -*-




import sys
import pyglet



#give me those
global document
global caret
global active


class Document(pyglet.event.EventDispatcher):
	"""
	subclass from Document,	implement append
	and set aside_tree.document to an instance of it
	"""
	def __init__(self):
		self.indentation = 0
		self.do_indent = True
		self.indent_length = 4
		#for kicking the cursor around:
		self.register_event_type('post_render')
		self.positions = {}
		
	def indent(self):
		self.indentation += 1
	def dedent(self):
		self.indentation -= 1
			
	def append(self, text, element, attributes={}):
		if not self.positions.has_key(element):
			self.positions[element] = caret.position
		a = {'element':element, 'color':element.color}
		#update merges attributes into a
		a.update(attributes)
		#did we append a newline earlier?
		if self.do_indent:   
			self.do_indent = False
			self._append(self.indent_spaces(), a)
		self.do_indent = (text == "\n")
		self._append(text, a)
			
	def indent_spaces(self):
		return self.indent_length*" " * self.indentation









class Element(pyglet.event.EventDispatcher):
	def __init__(self):
		super(Element,self).__init__()
		self.color = (200,255,200,255)
		self.children = {}
		self.parent = None
		self.register_event_types(
		'on_edit, on_text, on_text_motion, on_key_press, on_mouse_press')
	
	def __getattr__(self, name):

		if self.children.has_key(name):
			return self.children[name]
		else:
			raise AttributeError

	def set(self, key, item):
		self.children[key] = item
		item.parent = self

	def replace(self, item):
		self.parent.children[
				self.parent.children.values.index(self)
			] = item

	def dump(self):
		document.append(self.__repr__(), self)
		for item in self.children.itervalues():
			document.indent()
			if isinstance(item, Element):
				item.dump()
			else:
				print item.__repr__()
			document.dedent()

	def on_text(self, text):
		print "on_text default:", self, text
		return False
	
	def on_text_motion(self, motion, select=False):
		print "on_text_motion default:", self, (
			pyglet.window.key.motion_string(motion),
			select), " passing to caret"
		caret.on_text_motion(motion, select)
		return False

	def on_key_press(self, symbol, modifiers):
		print "on_key_press default:", self,(
			pyglet.window.key.modifiers_string(modifiers),
			pyglet.window.key.symbol_string(symbol))
		return False
		
	def on_mouse_press(self, x, y, button, modifiers):
		print "on_mouse_press default:", self, (
			x,y,button,modifiers)
		return False

	def is_caret_on_me(self):
		return active == self

	def register_event_types(self, types):
		for item in types.split(', '):
			self.register_event_type(item)







class piece(Element):
	pass

class t(piece):
	def __init__(self, text):
		self.text = text
	def render(self, node, _=None):
		document.append(self.text, node)
class s(piece):
	def render(self, node, lastitem):
		document.append(" ", node.children[lastitem.name])
	
class newline(piece):
	def render(self, node, _=None):
		document.append("\n" , node)#

class indent(piece):
	def render(self, node, _=None):
		document.indent()

class dedent(piece):
	def render(self, node, _=None):
		document.dedent()

class child(piece):
	def __init__(self, name):
		self.name = name
	def render(self, node, _=None):
		node.children[self.name].render()
	








class template(object):
	def __init__(self, items):
		self.items = items
	def render(self, node):
		if not isinstance(document, Document):
			raise Exception ("document is not Document")
		#print self.items
		lastitem = None #im going to hell for this lastitem thing
		for item in self.items:
			assert(isinstance(item, piece))
			item.render(node, lastitem)
			lastitem = item




"""
widgets
"""
class Widget(Element):
	pass




class TextWidget(Widget):
	def __init__(self, text):
		super(TextWidget, self).__init__()
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
		if (caret.get_style("element") != self) and (caret.get_style("piece") != self) 
			#raise Exception("caret isnt at me, dont ask me for position")
			return len(self.text)+1
		print "AA", caret.get_style("position")
		return caret.get_style("position")
		"""
		return caret.position - document.positions[self]

	def post_render_move_caret(self):
		if caret.get_style("element") != self:
			return

#		print "caret.position: ", caret.position
		
		m = self.post_render_move_caret
		self.post_render_move_caret = 0
		#move amount Node?:)

		if m == 0: return
#		print "move by: ", value

		if m < 0 and caret.position == 0:
			m = 0
		if m > 0 and caret.position == len(document.document.text):
			m = 0

		caret.position = caret.position + m
#		print self, "move by: ", value, " to ",caret.position
		
		
		
	def render(self):
		for position, letter in enumerate(self.text):
			document.append(self.text[position], self, {"position":position})
	
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



class ButtonWidget(Widget):
	def __init__(self, text="[🔳]"):
		super(ButtonWidget, self).__init__()
		self.color = (255,150,150,255)
		self.text = text
	def on_mouse_press(self, x, y, button, modifiers):
		print "button clicked"
		self.parent.clicked(self)
	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.RETURN:
			print "button pressed"
			self.parent.clicked(self)
	def render(self):
		document.append(self.text, self)
	
class NumberWidget(Widget):
	def __init__(self, text):
		super(NumberWidget, self).__init__()
		self.text = text
		self.set('minus_button', ButtonWidget("-"))
		self.addChildrenFromList(self.plus_button, self.minus_button)
	def render(self):
		self.minus_button.render()
		document.append(self.text, self)
		self.plus_button.render()
		








class AstNode(Element):
	def __init__(self):
		super(AstNode, self).__init__()
		self.color = (0,255,0,255)

class TextNode(AstNode):
	def __init__(self, value):
		super(TextNode, self).__init__()
		self.widget = TextWidget(value)
	def render(self):
		self.widget.render()


class TemplatedNode(AstNode):
	def __init__(self):
		super(TemplatedNode, self).__init__()
		self.template_index = 0
	template = property (lambda self: self.templates[self.template_index])
	def render(self):
		self.template.render(self)
	def prev_template(self):
		self.template_index  -= 1
		if self.template_index < 0:
			self.template_index = 0
	def next_template(self):
		self.template_index  += 1
		if self.template_index == len(self.templates):
			self.template_index = len(self.templates)-1
	def on_key_press(self, key, modifiers):
		if (pyglet.window.key.MOD_CTRL & modifiers) and (key == pyglet.window.key.UP):
			self.prev_template()
			print "prev"
		if (pyglet.window.key.MOD_CTRL & modifiers) and (key == pyglet.window.key.DOWN):
			self.next_template()
			print "next"




class NumberNode(AstNode):
	def __init__(self, value):
		super(NumberNode, self).__init__()
		self.value = value
		self.minus_button = ButtonWidget()
		self.plus_button = ButtonWidget()
	def render(self):
		document.append(str(self.value), self)




"""
#couple options:
store the positions of characters in an array ourselves - 
	hmm, this actually sounds pretty simple, might be dumping pyglets documents one day
store positions in attributes char by char
	for everything
	for just active.. nope...clicks...
"""




class ItemsNode(AstNode):
	def __init__(self, items):
		super(StatementsNode, self).__init__()
		self.items = items
		if not isinstance(items, list) and not isinstance(items, dict):
			raise Exception("parameter to StatementsNode constructor is not a list or dict")
		self.set('expand_collapse_button', ButtonWidget())
		self.expanded = False
		self.toggle_expanded()
	def render(self):
		document.dedent()

		padding = " " * (document.indent_length - 1)

		if self.expanded:
			self.expand_collapse_button.text = "-" + padding
		else:
			self.expand_collapse_button.text = "+" + padding

		self.expand_collapse_button.render()
		document.indent()
		if self.expanded:
			for item in self.items:
				item.render()
				newline().render(item)
		else:
			newline().render(self)
	
	def toggle_expanded(self):
		self.expanded = not self.expanded
	

	def clicked(self, item):
		if item is self.expand_collapse_button:
			self.toggle_expanded()






class DictNode(TemplatedNode):
	def __init__(self):
		super(DictNode, self).__init__()
		self.items = {}
		self.templates = [template([t("program by "),child("author"),s(),t("created on "),child("date_created"), newline(), indent(), child("statements"), dedent(), t("end.")]),
						template([t("lemon operating language running on python"), t(sys.version.replace("\n", "")), t(" ready."), newline(),indent(), child("statements"), dedent()])]
		self.set('statements', statements)
		self.set('author', TextWidget(author))
		self.set('date_created', TextWidget(date_created))



"""
now onto real programming
"""

class VariableReadNode(AstNode):
	def __init__(self, name):
		super(VariableReadNode, self).__init__()
		self.name = TextWidget(name)
	def render(self):
		self.name.render()

class RootNode(TemplatedNode):
	def __init__(self, statements, author="banana", date_created="1.1.1.1111"):
		super(RootNode, self).__init__()
		assert isinstance(statements, StatementsNode)

		self.templates = [template([t("program by "),child("author"),s(),t("created on "),child("date_created"), newline(), indent(), child("statements"), dedent(), t("end.")]),
						template([t("lemon operating language running on python"), t(sys.version.replace("\n", "")), t(" ready."), newline(),indent(), child("statements"), dedent()])]
		self.set('statements', statements)
		self.set('author', TextWidget(author))
		self.set('date_created', TextWidget(date_created))

class WhileNode(TemplatedNode):
	def __init__(self,condition,statements):
		super(WhileNode,self).__init__()

		self.templates = [template([t("while "), child("condition"), t(" do:"),indent(), newline(),child("statements"),dedent()]),
		template([t("repeat if "), child("condition"), t(" is true:"),indent(),newline(),child("statements"),dedent(),t("go back up..")])]
		self.set('condition', condition)
		self.set('statements', statements)


class AsignmentNode(TemplatedNode):
	def __init__(self, left, right):
		super(AsignmentNode,self).__init__()
		self.templates=[template([child("left"), t(" = "), child("right")]),
				template([t("set "), child("left"), t(" to "), child("right")]),
				template([t("have "), child("left"), t(" be "), child("right")])]
		self.set('left', left)
		self.set('right', right)
		
class IsLessThanNode(TemplatedNode):
	def __init__(self, left, right):
		super(IsLessThanNode,self).__init__()

		self.templates=[template([child("left"), t(" < "), child("right")])]
		self.set('left', left)
		self.set('right', right)
		

class PrintNode(TemplatedNode):
	def __init__(self,value):
		super(PrintNode,self).__init__()
	
		self.templates = [template([t("print "), child("value")]),
				template([t("say "), child("value")])]
		self.set('value', value)

"""
#set backlight brightness to %{number}%
self.templates = target.call_templates?
class CallNode(TemplatedNode):
	def __init__(self, target=):
		super(CallNode,self).__init__()
		self.target = target
		self.arguments = arguments
	def render(self):
		self.target
"""		
		
class UselessNode(TemplatedNode):
	def __init__(self):
		super(UselessNode,self).__init__()
	
class TodoNode(UselessNode):
	def __init__(self, text=""):
		super(TodoNode,self).__init__()
	
		self.templates = [template([t("todo: "), child("text")])]
		self.set('text', TextWidget(text))











class ShadowedTextWidget(TextWidget):

	def __init__(self, text, shadow):

		super(ShadowedTextWidget, self).__init__(text)
		self.shadow = shadow

	def render(self):

		document.append(self.text, self, {'color':self.color})
		document.append(self.shadow[len(self.text):], self, {'color':(130,130,130,255)})

	def len(self):
		return len(self.text+self.shadow[len(self.text)])
		


class MenuWidget(Widget):
	def __init__(self, items):
		super(MenuWidget, self).__init__()
		[self.register_event_type(i) for i in ['on_click']]
		self.color = (100,230,50,255)
		self.items = items
		self.sel = -1

	def render(self):
		for i, item in enumerate(self.items):
			#we will need to shift this here
			newline().render(self)
			document.append(item, self, 
				{'color':(255,100,100,255)} if self.sel == i else {})

		newline().render(self)
		
	

		

class PlaceholderNode(AstNode):
	def __init__(self, name="placeholder", type=None, default="None", example="None"):
		super(PlaceholderNode, self).__init__()
		self.default = default
		self.example = example
		self.set('textbox', ShadowedTextWidget("", "<<>>"))
		self.set('menu', MenuWidget([]))
		self.textbox.push_handlers(
			on_edit=self.on_widget_edit,
			on_text_motion=self.on_text_motion,
			on_key_press=self.on_key_press
			)

#		print self," items:"
#		for name, item in self.__dict__.iteritems():
#			print " ",name, ": ", item
	
	
	def on_widget_edit(self, widget):
		if widget == self.textbox:
			text = self.textbox.text
			self.menu.items = [text, text, text, text]
	
	def render(self):
		d = (" (default:"+self.default+")") if self.default else ""
		e = (" (for example:"+self.example+")") if self.example else ""

		x = d + e if active == self.textbox else ""


		self.textbox.shadow = "<<" + x + ">>"

		self.textbox.render()
#		print self.menu.items
		self.menu.render()


	def on_widget_text_motion(self, widget, motion, select):
#		print "~~~~~~~~~~~~~~~~~", motion
		
		if motion == pyglet.window.key.F1:
			self.menu.sel -= 1
		if motion == pyglet.window.key.F2:
			self.menu.sel += 1
			
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...
	
	







root = None

def populate_root():
	global root
	root = RootNode(StatementsNode([
		PlaceholderNode(), 
		AsignmentNode(TextNode("a"), NumberNode(1)),
		AsignmentNode(TextNode("b"), NumberNode(5)), 
		WhileNode(IsLessThanNode(VariableReadNode("a"), VariableReadNode("b")),
		StatementsNode([
			PrintNode(
			VariableReadNode("a")), 
			PlaceholderNode()])), 
		PlaceholderNode(),
		TodoNode("start looking into voice recognition:) (samson)")
		]))


"""










<AnkhMorporkian_> it's probably a bad idea to have newline as its own class. it'd be better to maintain it in the document class, since you have to have that anyways when you're using it.
<AnkhMorporkian> i understand why the nodes handle their own rendering, but I don't see why simple text characters should be.
<sirdancealot_> i wanted to have it uniform, to avoid special handling of str inside the template render







"""	
