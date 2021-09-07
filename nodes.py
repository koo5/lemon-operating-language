from collections import OrderedDict

import element
import widgets

class Node(element.Element):
	def __init__(self):
		super(Node, self).__init__()
		self.color = (0,255,0,255)

class Text(Node):
	def __init__(self, value):
		super(Text, self).__init__()
		self.widget = widgets.Text(value)
	def render(self):
		self.widget.render()

class Number(Node):
	def __init__(self, value):
		super(Number, self).__init__()
		self.value = value
		self.minus_button = widgets.Button()
		self.plus_button = widgets.Button()
	def render(self):
		document.append(str(self.value), self)

class Collapsible(Node):
	def __init__(self, items):
		super(Collapsible, self).__init__()
		self.items = items #do this first or bad things will happen
		self.set('expand_collapse_button', widgets.Button())
		self.expand_collapse_button.push_handlers(on_click=self.on_widget_click)
		self.expanded = True
	def render(self):
		self.expand_collapse_button.text = (
			("-" if self.expanded else "+") +
			(" " * (document.indent_length - 1)))
		self.expand_collapse_button.render()
		document.indent()
		if self.expanded:
			self.render_items()
		else:
			document.newline(self)
		document.dedent()
	
	def toggle(self):
		self.expanded = not self.expanded

	def on_widget_click(self, widget):
		if widget is self.expand_collapse_button:
			self.toggle()

class Dict(Collapsible):
	def __init__(self, *tuples):
		super(Dict, self).__init__(OrderedDict(tuples))
	def render_items(self):
			for key, item in self.items.items():
				document.append(key+":", self)
				if hasattr(item, "oneliner"):
					document.append(" ", self)
				else:
					document.append("\n", self)
				item.render()
				document.newline(item)
	def __getattr__(self, name):
		if name in self.items:
			return self.items[name]
		else:
			return super(Dict, self).__getattr__(name)

class List(Collapsible):
	def __init__(self, items):
		super(List, self).__init__(items)
		assert(isinstance(items, list))
	def render_items(self):
			for item in self.items:
				item.render()
				document.newline(item)

class CollapsibleText(Collapsible):
	def __init__(self, value):
		super(CollapsibleText, self).__init__(value)
		self.set('widget', widgets.Text(value))
	def render_items(self):
		self.widget.render()
		

class Statements(List):
	pass	

class VariableRead(Node):
	def __init__(self, name):
		super(VariableRead, self).__init__()
		self.name = widgets.Text(name)
	def render(self):
		self.name.render()

class Placeholder(Node):
	def __init__(self, name="placeholder", type=None, default="None", example="None"):
		super(Placeholder, self).__init__()
		self.default = default
		self.example = example
		self.set('textbox', widgets.ShadowedText("", "<<>>"))
		self.set('menu', widgets.Menu([]))
		self.textbox.push_handlers(
			on_edit=self.on_widget_edit,
			on_text=self.on_widget_text,
			)

#		print self," items:"
#		for name, item in self.__dict__.iteritems():
#			print " ",name, ": ", item
	
	
	def on_widget_edit(self, widget):
		if widget == self.textbox:
			text = self.textbox.text
#			self.menu.items = document.language.
	
	def render(self):
		d = (" (default:"+self.default+")") if self.default else ""
		e = (" (for example:"+self.example+")") if self.example else ""

		x = d + e if document.active == self.textbox else ""


		self.textbox.shadow = "<<" + x + ">>"

		self.textbox.render()
#		print self.menu.items
		self.menu.render()


	def on_widget_text(self, text):
		#use just shifts?
		if text == "T":
			self.menu.sel -= 1
			return True
		if text == "N":
			self.menu.sel += 1
			return True
			
	#def replace(self, replacement):
	#	parent.children[self.name] = replacement...
	
	

class Clock(Node):
	def __init__(self):
		super(Node,self).__init__()
		self.datetime = __import__("datetime")
	def render(self):
		document.append(str(self.datetime.datetime.now()), self)






