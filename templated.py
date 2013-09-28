
import widgets
from nodes import *
from templated_node import *

class Program(Templated):
	def __init__(self, statements, name="unnamed", author="banana", date_created="1.1.1.1111"):
		super(Program, self).__init__()
		assert isinstance(statements, Statements)
		self.sys=__import__("sys")
		self.templates = [template([t("program by "),child("author"),s(),t("created on "),child("date_created"), newline(), child("statements"), t("end.")]),
						template([t("lemon operating language running on python"), t(self.sys.version.replace("\n", "")), t(" ready."), newline(),child("statements")])]
		self.set('statements', statements)
		self.set('author', widgets.Text(author))
		self.set('date_created', widgets.Text(date_created))

class While(Templated):
	def __init__(self,condition,statements):
		super(While,self).__init__()

		self.templates = [template([t("while "), child("condition"), t(" do:"),newline(),child("statements")]),
		template([t("repeat if "), child("condition"), t(" is true:"),newline(),child("statements"),t("go back up..")])]
		self.set('condition', condition)
		self.set('statements', statements)


class Asignment(Templated):
	def __init__(self, left, right):
		super(Asignment,self).__init__()
		self.templates=[template([child("left"), t(" = "), child("right")]),
				template([t("set "), child("left"), t(" to "), child("right")]),
				template([t("have "), child("left"), t(" be "), child("right")])]
		self.set('left', left)
		self.set('right', right)
		
class IsLessThan(Templated):
	def __init__(self, left, right):
		super(IsLessThan,self).__init__()

		self.templates=[template([child("left"), t(" < "), child("right")])]
		self.set('left', left)
		self.set('right', right)
		

class Print(Templated):
	def __init__(self,value):
		super(Print,self).__init__()
	
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
		
class Useless(Templated):
	def __init__(self):
		super(Useless,self).__init__()
	
class Todo(Useless):
	def __init__(self, text="", priority = 1):
		super(Todo,self).__init__()
		if priority == 10:
			self.color=(255,0,0,255)
		self.templates = [template([t("todo: "), child("text")])]
		self.set('text', widgets.Text(text))
class Idea(Useless):
	def __init__(self, text=""):
		super(Idea,self).__init__()
	
		self.templates = [template([t("idea: "), child("text")])]
		self.set('text', widgets.Text(text))

