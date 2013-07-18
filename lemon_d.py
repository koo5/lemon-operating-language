#lemon operating language


#settings blocks

language:
	menu(item)


class slot():
	def __init__(self, type, multi):
		self.type = type
		self.multi = multi


class block(object):
	pass

class text_block_def(block):
	"""
	name
	texts[]
	"""
	def render(self):
		r = [gui.textbox(self.name), gui.text(":"), gui.newline()]
		for n, text in enumerate(texts):
			r = r + [gui.text("presentation "+n+":"), gui.newline()]
			for i in text:
				if i.class == gui.text:
					r.append(gui.textbox(i.text))



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




class gui_text():
	def __init__(self):
		self.text = "BANANA"
		self.color = pygame.Color("green")
	def len():
		return len(self.text)
	def draw(x,y):
		screen.surface.blit(font.render(self.text, antialias=True, self.color),(x,y))
class gui_focus():
	def __init__(self,text):
		self.color = (255,255,255)
		self.text = "↳"+text+"↲"
class gui_button
	def draw(x,y):
		pygame.gfxdraw.rectangle(screen, self.rect(x,y). pygame.Color("red"))
		gui_text.draw(self,x,y)
		
	def rect(x,y):
		return pygame.Rect(x,y,x+w(),y+h())

	def clickable(x,y):
		return (self.rect(), self.handler)
	
	def __init__(self, text, handler):
		self.handler = handler
		self.text = text

class gui_textbox



clickables = [] #(rect, handler)



def test_gui():
	class handler():
		click():
			print("yea")
	h = handler()
	render( [gui_text("bananas on fire"), gui_newline(),
		gui_button("click me if you can", h),
		gui_newline()] )
		



render(stuff):
	global clickables
	clickables = []
	x=0
	y=0

	for item in stuff:
		if y >= screen_y and y < screen_h:
			item.draw(topixels(x,y))
			if item.clickable:
				clickables[] = item.clickable(x,y)
		x = x + item.len()
	
		if isinstance(item, gui_newline):
			x=0
			y=y+1

click(x,y):
	for item in clickables:
		if item.collidepoint(x,y):
			item[1]()


def draw():
	screen_surface.fill((0,0,0))
