#!/usr/bin/python3
#-*- coding: utf-8 -*-
#lemon operating language bootstrap





import copy





contact = """
irc: sirdancealot @ freenode
https://github.com/koo5/lemon-operating-language
"""





def shit(gone_wrong):
	print(gone_wrong)
	print("\nfor support:",contact)





#indented (debug) output

def out(**args):
	print (["  "*indentation], args)

def ind(**args):
	global indentation
	out(args)
	indentation = indentation + 1

def ded(**args):
	global indentation
	out(args)
	indentation = indentation - 1








try:
	import pygame
	import pygame.gfxdraw
except:
	shit("i need pygame. please install pygame. sudo apt-get install pygame / yum install pygame ....")









def init_gui():
	global font
	global font_w
	global font_h
	global screen
	global screen_rows

	pygame.init()
	pygame.display.set_caption("lemon")#window title
	#sdl, which pygame is based on, has its own keyboard delay and repeat rate
	pygame.key.set_repeat(300,30)
	screen = pygame.display.set_mode((640,480))

	font = pygame.font.SysFont('monospace', 18)
	font_w = font.render(" ",False,(0,0,0)).get_rect().width
	font_h = font.get_height()
	screen_rows = screen.get_height() / font_h

	







lines = []
vscroll = 0 #amount of lines scrolled
done = False







def clear_lines():
	lines = [[] for i in range(0,screen_rows)]

#mostly everything is in chars, until inside the draw() functions
def topixels(x,y):
	return x * font_w, (y-screen_y) * font_h

#are we on screen?
def isvisible(x,y):
	return y >= vscroll and (y-vscroll) < screen_rows










class control(object):
	def __init__(self,parent):
		self.parent = parent
		self.controls = []
	def setparent(self, parent):
		self.parent = parent
		for c in self.controls:
			c.setparent(self)
	def imhere(self):
		lines[len(lines)-1].append(self)
	def copy(self):
		return copy.copy(self)


class text(control):
	def __init__(self, parent, text, color=pygame.Color("white")):
		super().__init__()
		self.text = text
		if isinstance(color, text):
			color = pygame.Color(color)
		self.color = color
	def len(self):
		return len(self.text)
	def render(self, (c,r)):
		if isvisible(c,r):
			screen.blit(font.render(self.text, True, self.color),topixels(c,r))
		return (c+self.len(),r)
	def rect(self, (c,r)):
		return pygame.Rect(c,r,font_width*self.len(),font_h)
		
class newline(control):
	def __init__(self,parent):
		super().__init__()
	def render(self, (c,r)):
		lines.append(list())
		return (0,r+1)
		
class button(text):
	def render(self, (c,r)):
		if isvisible(c,r):
			rect = self.rect(topixels(c,r))
			pygame.gfxdraw.rectangle(screen, rect, pygame.Color("red"))
			self.imhere()
		return super().render(self,(c,r))
		
	def __init__(self, parent, text, handler):
		super().__init__(parent, text)
		self.handler = handler

class textbox(text):
	def __init__(self, parent):
		super().__init__(parent)
		self.cursorx = 0
		
	def moveright(self):
		self.cursorx += 1

	def moveleft(self):
		if self.cursorx > 0: self.cursorx -= 1

	def keydown(self,k):
		if event.key==pygame.K_BACKSPACE:
			if cursorx > 0:
				self.text = self.text[0:cursorx-1]+self.text[cursorx:]
				cursorx -=1
		elif event.key==pygame.K_DELETE:
			if self.cursorx >= 0 and self.cursorx < len(self.text):
				self.text=self.text[0:self.cursorx]+self.text[self.cursorx+1:]
		elif event.unicode:
			self.text[0:self.cursorx]+event.unicode+self.text[cursorx:]
			cursorx +=1

	def render(self,(c,r)):
		if isvisible(c,r):
			px,py = topixels(c,r)
			#rectangle around
			pygame.draw.rect(screen,
				(0,255,0), (px,py,len(self.text)*font_w, font_h), 1)#thickenss

			#cursor
			startpos = (px+(self.cursorx*font_w), py)
			endpos   = (startpos[0],startpos[1]+font_h)
			pygame.draw.line(screen, (0, 155, 255), startpos, endpos, 3)#thickness
			self.imhere()
			
		return super().render(c+self.len(), r)


class block(control):
	def __init__(self, parent):
		super().__init__(parent)		
		self.gui = [gui_text(self,"im a block")]
	
	def setparent(self):
		super().setparent()
		print ("fixing gui orphans of ",self," (",self.gui,"):")
		for item in self.gui:
			print ("item ",item)
			item.setparent(self)

	def render(self,cr):
		cr = super().render()	
		for item in self.gui:
			cr = item.render(cr)
		return cr

	def keydown(e):
		print(e)
#		if e.key == pygame.K_UP:
#			self.parent.up()
#		if e.key == pygame.K_DOWN:
#			self.parent.down()
		

	
class block_list(block):
	def __init__(self):
		self.items = []
	def draw(self,(c,r)):
		for item in self.items:
			x,r = item.draw((c,r))
			r = r + 1
		return c,r
	def setparent(self):
		super().setparent()
		print ("fixing orphans (",self.items,") of ",self,"::")
		for item in self.items:
			print ("item ",item)
			item.parent = self
			item.fixorphans()



class template():
	def __init__(self, name, views):
		self.name = name
		self.views = views


		
class templated(block):
	def __init__(self,template):
		self.ancestor().__init__()
		self.template = template
		self.view = template.views[0]
		for item in self.view:
			j = item.copy()
			j.setparent(self)
			self.gui.append(j)



class template_editor(block):
	def __init__(self, parent, template):
		self.ancestor().__init__()
		self.template = template
		self.gui = [text(0,"ill be a template editor..one day!")]


class dummy(block):
	def __init__(self, parent, text):
		self.gui = [text(self, "<<"+text+">>",(250,250,200)]
		self.parent = parent
	
	def keydown(e):
		if e.unicode:
			a = inputty(self.parent)
			self.parent.replace(self,a)
			a.keydown(e)
		else:
			parent.keydown(e)

class menu():
	def __init__(self, parent):
		self.parent = parent
		
	
	def setitems(self, items):
		self.items = items
	
	def keydown(self, e):
		if e.key == pygame.K_DOWN:
			self.sel = self.sel +1
		if e.key == pygame.K_UP:
			self.sel = self.sel -1
	
	def draw(self, cr):
		n=0
		for text, val in self.items:
			text(self, text, "white" if n == self.sel else "yellow").draw(cr)
			cr = (c,r+1)
			n=n+1



class block_inputty(block):
	def __init__(self):
		self.gui = [textbox(self,"inputty"), newline(self), menu(self)]


	def keydown(self,e):
		self.gui[0].keydown(e) | self.gui[1].keydown(e)
		


root = block_list()

root.items.append(
	template_editor(0,template("if",
			[[
			gui_text(0,"if "), 
			block_dummy(0,"condition"),
			gui_newline(0), 
			block_dummy(0,"then")
			]])))

root.items.append(templated_block(root.items[0].template))

root.items.append(block_dummy(0))

focused = root.items[0]

root.fixorphans()

"""
dummy is focused
key is pressed
menu is displayed
item is selected
dummy is replaced
...
"""






def draw():
	clear_lines()
	screen.fill((0,0,0))
	root.draw((0,0))
	pygame.display.update()




def bye():
	global done
#	if __name__ == "__main__":
#		exit()
#	else:
	done = True


def keydown(event):
	focused.keydown()


	
def click(pos):
	x,y=pos
	print (x,y,clickables)
	for item in clickables:
		if item[0].collidepoint(x,y):
			print(item[0])
			item[0].click()



def process_event(e):
	if e.type == pygame.MOUSEBUTTONDOWN:
		click(e.pos)
	elif e.type == pygame.QUIT:
		exit()
#y u no work
#	elif e.type == pygame.VIDEOEXPOSE:
#		draw()
	elif e.type == pygame.KEYDOWN:
		keydown(e)


def loop():
	process_event(pygame.event.wait())
	draw()


def main():
	init_gui()
	pygame.time.set_timer(pygame.USEREVENT, 1000)#40)#SIGINT timer
	while not done:
		try:
			loop()
		except KeyboardInterrupt() as e:
			pygame.display.iconify()
			raise e
		except Exception() as e:
			pass







class language():
	#menu(item)
	pass
	#sooomewhere over the rainbow


#block view editor
#class block_def(block):
#	"""
#	name
#	views[]
#	"""
#	def update_gui(self):
#		self.gui = [gui_text("blockt type: "), gui_textbox(self.name), gui_text(":"), gui_newline()]
#		self.gui = [gui_text("children: "), gui_newline()]
#		for n, view in enumerate(views):
#			self.gui = self.gui + [gui_text("view "+n+":"), gui_newline()]
#			for i in view:
#				if i.class == gui.text:
#					self.gui.append(gui.textbox(i.text))
#			self.gui = self.gui + [gui_newline()]
