##!/usr/bin/python3
#-*- coding: utf-8 -*-
#lemon operating language bootstrap






contact = """
irc: sirdancealot @ freenode
https://github.com/koo5/lemon-operating-language
"""





def shit(gone_wrong):
	print(gone_wrong)
	print("\nfor support:",contact)







try:
	import pygame
	import pygame.gfxdraw
except Exception as e:
	shit("i need pygame. please install pygame. sudo apt-get install pygame / yum install pygame ....")
	raise(e)

import copy







lines = []
vscroll = 0 #amount of lines scrolled
done = False
fline = 0
fitem = None
tab = 3







#syntax sugar

class banana(object):
	"""
	aaa = banana()
	aaa.bbb = 555
	print aaa.bbb
	"""
	def __setattr__(s, n, v):
		s.__dict__.update({n:v})







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









def init_gui():
	global font
	global font_w
	global font_h
	global screen
	global screen_rows
	global screen_cols
	global screen_w
	global screen_h

	pygame.init()
	pygame.display.set_caption("lemon")#window title
	#sdl, which pygame is based on, has its own repeat delay and repeat rate
	pygame.key.set_repeat(300,30)

	screen_w = 640
	screen_h = 480
	
	screen = pygame.display.set_mode((screen_w,screen_h))

	font = pygame.font.SysFont('monospace', 18)
	font_w = font.render(" ",False,(0,0,0)).get_rect().width
	font_h = font.get_height()
	screen_rows = screen_h / font_h
	screen_cols = screen_w / font_w

	








#mostly everything is in chars, until inside the draw() functions
def topixels(x,y):
	return x * font_w, (y-vscroll) * font_h

#are we on screen?
def isvisible(x,y):
	return y >= vscroll and (y-vscroll) < screen_rows










class control(object):
	def __init__(self,parent):
		self.parent = parent
		self.children = [label(self, self.__repr__())]
		self.last = banana()
	def setparent(self, parent):
		self.parent = parent
		for c in self.children:
			c.setparent(self)
	def imhere(self,c,r):
		lines[r].append(self)
		self.last.rect = self.rect()
	def copy(self):
		return copy.copy(self)
		print "hmm"
	def render(s, c,r):
		for item in self.children:
			c,r = item.render(c,r)
		self.imhere(r)
		return c,r
		

class block(control):
	def __init__(self, parent):
		super(block,self).__init__(parent)
		self.gui = [label(self, self.__repr__()),newline(self)]
	

	def keydown(e):
		print(e)
#		if e.key == pygame.K_UP:
#			self.parent.up()
#		if e.key == pygame.K_DOWN:
#			self.parent.down()
		



class label(control):
	def __init__(self, parent, text, color=pygame.Color("white")):
		super(label,self).__init__(parent)
		self.text = text
		if isinstance(color, str):
			color = pygame.Color(color)
		self.color = color
	def len(self):
		return len(self.text)
	def render(self, c,r):
		if isvisible(c,r):
			screen.blit(font.render(self.text, True, self.color),topixels(c,r))
			self.imhere()
		return (c+self.len(),r)
	def rect(self, c,r):
		return pygame.Rect(c,r,font_width*self.len(),font_h)


class newline(control):
	def __init__(self,parent):
		super(self.__class__,self).__init__(parent)
#	def render(self, c,r):
#		return (0,r+1)
		
class button(label):
	def render(self, c,r):
		if isvisible(c,r):
			rect = self.rect(topixels(c,r))
			pygame.gfxdraw.rectangle(screen, rect, pygame.Color("red"))
			self.imhere(r)
		return super(self.__class__,self).render(self,c,r)
		
	def __init__(self, parent, text):
		super(self.__class__,self).__init__(parent, text)

class textbox(label):
	def __init__(self, parent):
		super(self.__class__,self).__init__(parent)
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

	def render(self,c,r):
		if isvisible(c,r):
			px,py = topixels(c,r)
			#rectangle around
			pygame.draw.rect(screen,
				(0,255,0), (px,py,len(self.text)*font_w, font_h), 1)#thickenss

			#cursor
			startpos = (px+(self.cursorx*font_w), py)
			endpos   = (startpos[0],startpos[1]+font_h)
			pygame.draw.line(screen, (0, 155, 255), startpos, endpos, 3)#thickness
			self.imhere(r)
			
		return super(self.__class__,self).render(c+self.len(), r)


	def rect(self, c,r):
		return pygame.Rect(c,r,font_width*self.len(),font_h)

	
class block_list(block):
	def __init__(i,parent,items,indent=tab):
		super(block_list,i).__init__(parent)
		i.items = items
		i.indent = indent
		i.controls = [button
	def setparent(i,parent):
		super(block_list,i).setparent(parent)
		print ("fixing orphans (",i.items,") of ",i,"::")
		for item in i.items:
			print ("item ",item)
			item.setparent(i)

	def render(i,c,r):
		c,r=super(block_list,i).render(c,r)
		for item in i.items:
			_,r = item.render(c+i.indent, r)
			r=r+1
		return c,r


class template():
	def __init__(self, name, views):
		self.name = name
		self.views = views


		
class templated(block):
	def __init__(self,parent,template):
		super(templated,self).__init__(parent)
		self.template = template
		self.view = template.views[0]
		for item in self.view:
			j = item.copy()
			print j
			j.setparent(parent)
			self.gui.append(j)



class template_editor(block):
	def __init__(self, parent, template):
		super(template_editor,self).__init__(parent)
		self.template = template
		self.gui = [label(0,"ill be a template editor..one day!")]


class dummy(block):
	def __init__(self, parent, text):
		super(dummy,self).__init__(parent)
		self.gui = [label(self, "<<"+text+">>",(250,250,200))]
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
	
	def draw(self, c,r):
		n=0
		for text, val in self.items:
			label(self, text, "white" if n == self.sel else "yellow").draw(cr)
			c,r = (c,r+1)
			n=n+1



class block_inputty(block):
	def __init__(self):
		self.gui = [textbox(self,"inputty"), newline(self), menu(self)]


	def keydown(self,e):
		self.gui[0].keydown(e) | self.gui[1].keydown(e)
		


root = block_list(0, [template_editor(0,template("if",
			[[
			label(0,"if "), 
			dummy(0,"condition"),
			newline(0), 
			block_list(0,[dummy(0,"then")])
			]]))
		     ],1)

root.items.append(templated(0,root.items[0].template))

root.items.append(dummy(0,"BANANA"))

focused = root.items[0]

root.setparent(0)

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
	
	pygame.gfxdraw.rectangle(screen, (0, fline * font_h, screen_w,  font_h), pygame.Color("red"))

	if focus != None:
		pygame.gfxdraw.rectangle(screen, (0, fline * font_h, screen_w,  font_h), pygame.Color("red"))
	
	root.render(0,0)
	pygame.display.update()




def bye():
	global done
#	if __name__ == "__main__":
#		exit()
#	else:
	done = True



def clear_lines():
	global lines
	lines = [[] for i in range(0,screen_rows)]
	print lines


def activate():
	global focus
	print lines
	if len(lines[fline]) > 0:
		focus = lines[fline][0]


def keydown(e):
	global fline
	if e.key == pygame.K_UP:
		if fline > 0:
			fline -= 1
			activate()
	if e.key == pygame.K_DOWN:
		if fline < screen_rows-1:
			fline += 1
			activate()

#	focused.keydown()

	
def click(pos):
	for line in lines:
		for item in line:
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
		if e.key == pygame.K_ESCAPE:
			exit()
		else:
			keydown(e)


def loop():
	draw()
	process_event(pygame.event.wait())


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
