#!/usr/bin/env python
# -*- coding: utf-8 -*-



#lets ingraft this onto the element tree






global document
global caret

"""
subclass from Document, implement append and set aside_tree.document to it
"""
class Document(object):
	def __init__(self):
		self.indentation = 0
		self.on_a_new_line = True
		self.indent_length = 4
	def indent(self):
		self.indentation += 1
	def dedent(self):
		self.indentation -= 1
	def append(self, text, attributes):
		if self.on_a_new_line:
			self.on_a_new_line = False
			self._append(self.return_indent(), attributes)
			self.on_a_new_line = (text == "\n")
	def indent_spaces(self):
		return " "*self.indent_length













class Element(object):
	def on_text(self, motion):
		print self, motion
	
	def on_text_motion(self, motion, select=False):
		print self, motion, select







class piece(Element):
	pass

class t(piece):
	def __init__(self, text):
		self.text = text
	def render(self, node):
		document.append(self.text, {"element":node})

class newline(piece):
	def render(self, node):
		document.append("\n" , {"element":node})#

class indent(piece):
	def render(self, node):
		document.indent()

class dedent(piece):
	def render(self, node):
		document.dedent()

class child(piece):
	def __init__(self, name):
		self.name = name
	def render(self, node):
		print node.__dict__[self.name]
		node.__dict__[self.name].render()
	








class template(object):
	def __init__(self, items):
		self.items = items
	def render(self, node):
		assert isinstance(document, Document)
		for item in self.items:
			assert(isinstance(item, piece))
			item.render(node)




"""
widgets
"""
class Widget(Element):
	pass

class TextWidget(Widget):
	def __init__(self, text):
		self.text = text

	@property
	def caret_position(self):
		if caret.get_style("element") != self:
			raise Exception("caret isnt at me, dont ask me for position")
		return caret.get_style("position")

	@caret_position.setter
	def set_caret_position(self, value):
		caret.position = caret.position - value
	
		
	def render(self):
		for position, letter in enumerate(self.text):
			document.append(self.text, {"element":self})
#			, "position":self.caret_position})
	
	def on_text(self, text):
		pos = self.caret_position
		self.caret_position += len(text)
		self.text = self.text[:pos] + text + self.text[pos:]
		parent.on_edit(self)
	
	def on_text_motion(self, motion, select=False):
		if motion == key.MOTION_BACKSPACE:
			if self.caret_position > 0:
				self.caret_position -= 1
				self.text = self.text[:position-1]+self.text[position:]
		if motion == key.MOTION_LEFT:
			self.caret_position = max(0, self.caret_position - 1)
		elif motion == key.MOTION_RIGHT:
			self.caret_position = min(len(self.text), self.caret_position + 1)

	"""
		emits on_edit
	"""




class ButtonWidget(Widget):
	def __init__(self, text="[🔳]"):
		self.text = text
	def on_click(self):
		parent.clicked(self)
	def render(self):
		document.append(self.text, {"element":self})
	
class NumberWidget(Widget):
	def __init__(self, text):
		self.text = text
		self.plus_button = ButtonWidget()
		self.minus_button = ButtonWidget()
	def render(self):
		self.minus_button.render()
		document.append(self.text, {"element":self})
		self.plus_button.render()
		








class AstNode(Element):
	pass

class TextNode(AstNode):
	def __init__(self, value):
		self.widget = TextWidget(value)
	def render(self):
		self.widget.render()

class PlaceholderNode(AstNode):
	def __init__(self, name="placeholder", type=None, default=None, example=None):
		d = (" (default:"+default+")") if default else ""
		e = (" (for example:"+example+")") if example else ""
		self.widget = TextWidget("<<"+name+d+e+">>")
	
	def render(self):
		self.widget.render()
		
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...
	#def on_text(self, text):
	#	print "plap"
	
	def on_edit(self, widget):
		print "show menu"
	
	

class TemplatedNode(AstNode):
	def __init__(self):
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
	def on_keypress(self, key, modifiers):
		if pyglet.MOD_CTRL in modifiers and key == pyglet.UP:
			prev_template()
		if pyglet.MOD_CTRL in modifiers and key == pyglet.DOWN:
			next_template()





class NumberNode(AstNode):
	def __init__(self, value):
		self.value = value
		self.minus_button = ButtonWidget()
		self.plus_button = ButtonWidget()
	def render(self):
		document.append(str(self.value), {"element":self})



class StatementsNode(AstNode):
	def __init__(self, items):
		self.items = items
		if not isinstance(items, list):
			raise Exception("parameter to statements_node constructor is not a list")
		self.expand_collapse_button = ButtonWidget()
		self.expanded = False
		self.toggle_expanded()
	def render(self):
		document.dedent()
		self.expand_collapse_button.render()
		document.append(document.indent_spaces()[len(self.expand_collapse_button.text)], {"element":self})
		document.indent()
		if self.expanded:
			for item in self.items:
				item.render()
				newline().render(self)
	def toggle_expanded(self):
		self.expanded = not self.expanded
		if not self.expanded:
			self.expand_collapse_button.text = "+++"
		else:
			self.expand_collapse_button.text = "---"
	
	def clicked(self, item):
		if item == self.expand_collapse_button:
			self.toggle_expanded()





class VariableReadNode(AstNode):
	def __init__(self, name):
		self.name = TextWidget(name)
	def render(self):
		self.name.render()








"""
now onto real programming
"""


class RootNode(TemplatedNode):
	def __init__(self, statements, author="banana", date_created="1.1.1.1111"):
		super(RootNode, self).__init__()
		assert isinstance(statements, StatementsNode)

		self.templates = [template([t("program by "),child("author"), t(" created on "), child("date_created"), newline(), indent(), child("statements"), dedent(), t("end.")])]
		self.statements = statements
		self.author = TextWidget(author)
		self.date_created = TextWidget(date_created)

class WhileNode(TemplatedNode):
	def __init__(self,condition,body):
		super(WhileNode,self).__init__()

		self.templates = [template([t("while "), child("condition"), t(" do:"),indent(), newline(),child("body"),dedent()]),
		template([t("repeat if"), child("condition"), t("is true:"),child("body"),t("go back up..")])]
		self.condition = condition
		self.body = body


class AsignmentNode(TemplatedNode):
	def __init__(self, left, right):
		super(AsignmentNode,self).__init__()
		self.templates=[template([child("left"), t(" = "), child("right")]),
				template([t("set "), child("left"), t(" to "), child("right")]),
				template([t("have "), child("left"), t(" be "), child("right")])]
		self.left=left
		self.right=right
		
class IsLessThanNode(TemplatedNode):
	def __init__(self, left, right):
		super(IsLessThanNode,self).__init__()

		self.templates=[template([child("left"), t(" < "), child("right")])]
		self.left=left
		self.right=right
		

class PrintNode(TemplatedNode):
	def __init__(self,value):
		super(PrintNode,self).__init__()
	
		self.templates = [template([t("print "), child("value")]),
				template([t("say"), child("value")])]
		self.value = value



root = RootNode(StatementsNode([AsignmentNode(TextNode("a"), NumberNode(1)),
									AsignmentNode(TextNode("b"), NumberNode(5)), 
									WhileNode(IsLessThanNode(VariableReadNode("a"), VariableReadNode("b")),
									StatementsNode([
									PrintNode(
									VariableReadNode("a")), 
									PlaceholderNode()])), 
									PlaceholderNode()]))




"""


<AnkhMorporkian_> it's probably a bad idea to have newline as its own class. it'd be better to maintain it in the document class, since you have to have that anyways when you're using it.
<AnkhMorporkian> i understand why the nodes handle their own rendering, but I don't see why simple text characters should be.
<sirdancealot_> i wanted to have it uniform, to avoid special handling of str inside the template render


"""	
