#settings blocks

language:
	menu(item)


class slot():
	def __init__(self, type, multi):
		self.type = type
		self.multi = multi


block:
	"""abstract presentation()


text_presented_block_type(block):
	"""
	name
	presentations[]
	"""



text_presented_block(block):
	presentation():
		res = []
		for item in self.type.presentation[self.presentationid]:
			if isinstance(item, str):
				res[] = item
			elif isinstance(item, block):
				res[] = item.presentation()

printroot():
	for item in root.presentation():
		if item == focus:
			sys.stdout.write(">>"+item+"<<")
		else
			sys.stdout.write(item)



class program(block):
	def presentation
	
	

"""
!!python:__lemon_d__.program




!!python:__lemon_d__.typedblock
type: root
items:
	!!python:__lemon_d__.blocklist
	items:
		-
			!!python:__lemon_d__.blocktype
			name: root
			presentations: [[
#serialization sucks
"""

#clickables = array of (x,y,x,y) tuples


class gui_text():
	def sim(x,y):
		x=x+len(self.text)
		y=y+self.text.count("\n")
		return x,y
class gui_focus():
	color = (255,255,255)
class gui_button
	def clickable():
		return (pygame.Rect(
class gui_textbox




render(stuff):
	x=0
	y=0
	clickables = []
	for item in stuff:
		if y >= screen_y and y < screen_h:
			x,y=item.draw(x,y)
		else:
			x,y=item.sim(x,y)
	
		if isinstance(item, text):
			out += item
		elif isinstance(item, ):
			out += item
		
