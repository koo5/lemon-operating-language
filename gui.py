#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
#lemon operating language bootstrap gui toolkit


from __future__ import print_function


try:
	import pygame
	import pygame.gfxdraw
except:
	shit("i need pygame. please install pygame. sudo apt-get install pygame / yum install pygame ....")


contact = """

irc: sirdancealo* @ freenode
https://github.com/koo5/lemon-operating-language
"""


def shit(gone_wrong):
	print(gone_wrong)
	print("\nfor support:",contact)



config = dict()
try:
	config = __import__("config").__dict__
except:
	pass



def init_gui():
	global font
	global font_width
	global screen
	global screen_h

	pygame.init()
	pygame.display.set_caption("lemon")#window title
	#sdl, which pygame is based on, has its own keyboard delay and repeat rate
	pygame.key.set_repeat(config.get("delay") or 300,config.get("rate") or 30)
	#this creates a window, so sorry for the size hardcoding for now
	screen = pygame.display.set_mode((640,480))


	#the final version is planned to use comic sans ✈
	font = pygame.font.SysFont('monospace', 17)
	font_width = font.render(" ",False,(0,0,0)).get_rect().width

	screen_h = screen.get_height() / font.get_height()

	


clickables = [] #(rect, handler)
screen_y = 0 #scroll in lines


def topixels(x,y):
	return x * font_width, (y-screen_y) * font.get_height()







class gui_text(object):
	def __init__(self, text):
		self.text = text
		self.color = pygame.Color("green")
	def len(self):
		return len(self.text)
	def draw(self, (x,y)):
		screen.blit(font.render(self.text, True, self.color),(x,y))
class gui_newline():
	def draw(self, (x,y)):
		pass
class gui_focus(gui_text):
	def __init__(self,text):
		self.color = (255,255,255)
		self.text = "↳"+text+"↲"
class gui_button(gui_text):
	def draw(self, (x,y)):
		pygame.gfxdraw.rectangle(screen, self.rect(x,y), pygame.Color("red"))
		print (self.rect(x,y))
		gui_text.draw(self,(x,y))
		
	def rect(self, x,y):
		return pygame.Rect(x,y,font_width*self.len(),font.get_height())

	def clickable(self, (x,y)):
		return (self.rect(x,y), self.handler)
	
	def __init__(self, text, handler):
		gui_text.__init__(self, text)
		self.handler = handler

#class gui_textbox():

done = False

def bye():
	global done
	if __name__ == "__main__":
		exit()
	else:
		done = True





def render(stuff):
	global clickables
	clickables = []
	x=0
	y=0

	for item in stuff:
		if isinstance(item, gui_newline):
			x=0
			y=y+1
		else:
			if y >= screen_y and y < screen_h:
				item.draw(topixels(x,y))
				if hasattr(item,'clickable'):
					print(item.clickable(topixels(x,y)))
					clickables.append(item.clickable(topixels(x,y)))
			x = x + item.len()
	
def click(pos):
	x,y=pos
	print (x,y,clickables)
	for item in clickables:
		if item[0].collidepoint(x,y):
			print(item[1])
			item[1].click()


def draw():
	screen.fill((0,0,0))

	class handler(object):
		def click(self):
			print("yea")
	h = handler()

	render( [gui_text("bananas on fire"), gui_newline(),
		gui_button("click me if you can", h),
		gui_newline()] )	

	pygame.display.update()

def process_event(e):
	if e.type == pygame.MOUSEBUTTONDOWN:
		click(e.pos)
	elif e.type == pygame.QUIT:
		exit()
#	elif e.type == pygame.VIDEOEXPOSE:
#		draw()

def loop():
	process_event(pygame.event.wait())
	draw()

def main():
	pygame.time.set_timer(pygame.USEREVENT, 1000)#40)#SIGINT timer
	while not done:
		try:
			loop()
		except KeyboardInterrupt() as e:
			pygame.display.iconify()
			raise e
		except Exception() as e:
			pass

def test_gui():
	init_gui()
	main()

if __name__ == "__main__":
	test_gui()

