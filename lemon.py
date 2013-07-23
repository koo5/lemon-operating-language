#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
#lemon operating language bootstrap


from __future__ import print_function
from copy import deepcopy


contact = """
irc: sirdancealot @ freenode
https://github.com/koo5/lemon-operating-language
"""



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




def shit(gone_wrong):
	print(gone_wrong)
	print("\nfor support:",contact)



try:
	import pygame
	import pygame.gfxdraw
except:
	shit("i need pygame. please install pygame. sudo apt-get install pygame / yum install pygame ....")




config = dict()
try:
	config = __import__("config").__dict__
except:
	pass



def init_gui():
	global font
	global font_w
	global font_h
	global screen
	global screen_h

	pygame.init()
	pygame.display.set_caption("lemon")#window title
	#sdl, which pygame is based on, has its own keyboard delay and repeat rate
	pygame.key.set_repeat(config.get("delay") or 300,config.get("rate") or 30)
	#this creates a window, so sorry for the size hardcoding for now
	screen = pygame.display.set_mode((640,480))


	#the final version is planned to use comic sans ✈
	font = pygame.font.SysFont('monospace', 18)
	font_w = font.render(" ",False,(0,0,0)).get_rect().width
	font_h = font.get_height()

	screen_h = screen.get_height() / font.get_height()

	

done = False
clickables = [] #(handler, rect)
screen_y = 0 #amount of lines scrolled


#mostly everything is in chars, until inside the draw() functions
def topixels(x,y):
	return x * font_w, (y-screen_y) * font_h

#are we on screen?
def isvisible(x,y):
	return y >= screen_y and y < screen_h



#gui controls


class gui_text(object):
	def __init__(self, parent, text, color=pygame.Color("green")):
		self.parent = parent
		self.text = text
		self.color = color
	def len(self):
		return len(self.text)
	def draw(self, (c,r)):
		if isvisible(c,r):
			screen.blit(font.render(self.text, True, self.color),topixels(c,r))
		return (c+self.len(),r)
class gui_newline():
	def __init__(self,parent):
		self.parent = parent
	def draw(self, (c,r)):
		return (0,r+1)
class gui_focus(gui_text):
	def __init__(self,parent,text):
		self.color = (255,255,255)
		self.text = "↳"+text+"↲"
		self.parent = parent
class gui_button(gui_text):
	def draw(self, (c,r)):
		global clickables
		if isvisible(c,r):
			rect = self.rect(topixels(c,r))
			clickables.append((self.handler, rect))
			pygame.gfxdraw.rectangle(screen, rect, pygame.Color("red"))
		return gui_text.draw(self,(c,r))
		
	def rect(self, (c,r)):
		return pygame.Rect(c,r,font_width*self.len(),font_h)

	def __init__(self, parent, text, handler):
		gui_text.__init__(self, text)
		self.handler = handler
		self.parent = parent


class gui_textbox(gui_text):

	def __init__(self, parent):
		self.cursorx = 0
		self.parent = parent
		
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

	def draw(self,(c,r)):
		if isvisible(c,r):
			px,py = topixels(c,r)
			#rectangle around
			pygame.draw.rect(screen,
				(0,200,0), (px,py,len(self.text)*font_w, font_h), 1)#thickenss

			#text
			screen.blit(font.render(self.text,True,self.color),(px, py))
		
			#cursor
			startpos = (px+(self.cursorx*font_w), py)
			endpos   = (startpos[0],startpos[1]+font_h)
			pygame.draw.line(screen, (0, 255, 0), startpos, endpos, 3)#thickness
		
		return (c+self.len(), r)



class gui_child():
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
	
	def draw(c,r):
		return parent.__dict__()[self.name].draw(c,r)




class block(object):
	def ancestor(self):
	#wont this always work with block?
		print ("my ancestor is ",super(type(self),self))
		return super(type(self),self)

	def fixorphans(self):
		print ("fixing gui orphans of ",self," (",self.gui,"):")
		for item in self.gui:
			print ("item ",item)
			item.parent = self

	def __init__(self):
		self.gui = [gui_text(self,"im a block")]
	
	def draw(self,cr):
		for item in self.gui:
			cr = item.draw(cr)
		return cr

	def copy_gui():
		self.gui = self.type.views[self.viewid][:]
	
	def keydown(e):
		pass
		#print( "banana")
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
	def fixorphans(self):
		print ("fixing orphans (",self.items,") of ",self,"::")
		for item in self.items:
			print ("item ",item)
			item.parent = self
			item.fixorphans()


class template():
	def __init__(self, name, views):
		self.name = name
		self.views = views
		self.kids = [] #template kids are not to be confused with block children
		#supposing all views show the same children
		for item in views[0]:
			if isinstance(item, gui_child):
				self.kids.append(item.name)

		
class templated_block(block):
	def __init__(self,template):
		self.ancestor().__init__()
		self.template = template
		self.children = {}
		self.view = template.views[0]
		for item self.view:
			j = deepcopy(item)
			j.parent = self
			self.gui.append(j)
			if isinstance(item, gui_child):
			
			
		for item in template.kids:
			self.children[item] = block_dummy(self)
		for i in template.views[0]:

	def fixorphans(self):
		print ("fixing orphans (",self.children,") of ",self,"::")
		for name, item in self.children.iteritems():
			print ("item ",item)
			item.parent = self
			item.fixorphans()
		block.fixorphans(self)



class template_editor(block):
	def __init__(self, parent, template):
		self.parent = parent
		self.template = template
		self.gui = [gui_text(0,"im a template editor!")]


class block_dummy(block):
	def __init__(self, parent):
		self.gui = [gui_text(self, "dummy")]
		self.parent = parent
	
	def keydown(e):
		if e.unicode:
			a = gui_inputty(self.parent)
			self.parent.replace(self,a)
			a.keydown(e)
		else:
			parent.keydown(e)

class gui_menu():
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
			if n == self.sel:
				c = pygame.Color("white")
			else:
				c = pygame.Color("yellow")
			gui_text(self, text, c).draw(cr)
			cr = (c,r+1)
			n=n+1
			


class block_inputty(block):
	def __init__(self):
		self.gui = [gui_textbox(self,"inputty"), gui_newline(self), gui_menu(self)]


	def keydown(self,e):
		self.gui[0].keydown(e) | self.gui[1].keydown(e)
		


root = block_list()

root.items.append(
	template_editor(0,template("if", 
			[[
			gui_text(0,"if "), 
			gui_dummy(0,"condition"),
			gui_newline(0), 
			gui_dummy(0,"then")
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
	global clickables
	clickables = []
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
