from nodes import *

"""
menu(type, start):
	
	
	variables, functions, types
	
	
	placeholder type:
		statement:
			for, if, while, def, call, 
			
			
			
			asignment:
				variables in scope:
					for item above me:
						 
		
			call:
				functions in scope:
					for item in program:
						if item is defun:
							+
		
		expression:
			bracket, operators, functions with return types, literals, variables		



def scope(item):
	items = [i for i in walkup(item)]



def walkup(item):
	if isinstance(item.parent, List):
		for i in range(item.parent.indexof(self, 



def functions(node):
	result = []
	program = node.program()
	for item in program.statements.items: #walk top level statements
		if isinstance(item, nodes.FunctionDefinition):
			result += item
	return result


#Use(Module(


constructs = [nodes.If]


class While(Templated):
	templates = [
					template([t("while "), child("condition"), t(" do:"),newline(),child("statements")]),
					template([t("repeat if "), child("condition"), t(" is true:"),newline(),child("statements"),t("go back up..")])
				]

	def __init__(self,condition,statements):
		super(While,self).__init__()
		self.set('condition', condition)
		self.set('statements', statements)




def templates(text):
	for c in :
		for template in c.templates:
			for i in template:
				if isinstance(i,t):



for d in definitions visible by program:



every program




builtin library is visible by every program




if module == builtin:
	case function in:
		if:
		while:
		defun:
		
"""


syntax = {
	'statements': [If, While, Asignment],
	'expressions': [IsLessThan, VariableRead]
}


def add(name, array):
	ret = []
	for node in array:
		for template in node.templates:
			ret += name + ": " + node.__name__ + ": "

def menu(name):
	ret = add(name, syntax[name])
	for k,i in syntax.iteritems():
		if k != name:
			ret = ret + add(k, i)

