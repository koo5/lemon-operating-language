__author__ = 'ankhmorporkian & sirdancealot'
from lemon_logger import LemonLogger
from element import *
from clock import Clock

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

logger = LemonLogger()


class EditorWindow(pyglet.window.Window):
    """
    Editor class, creates an editing window for the lemon language.
    """

    def __init__(self, title='Lemon editor', font_name="monospace", font_size=18):
        super(EditorWindow, self).__init__(caption=title,
                                           resizable=True)
        self.setupGl()
        self.setFont(font_name, font_size)
        self.root_element = Element(root = True)
        Clock(self.root_element)
        self.root_element.setPosition(0,0)

    def setupGl(self):
        glClearColor(0, 0, 0, 1)

    def setFont(self, font_name="monospace", font_size=18):
        self.font_name = font_name
        self.font_size = font_size
#        self.letter_width = self.font.render(" ",False,(0,0,0)).get_rect().width
#        self.letter_height = self.font.get_height()

    def on_resize(self, width, height):
        super(EditorWindow, self).on_resize(width, height)

    def on_draw(self):
        #glClear(GL_COLOR_BUFFER_BIT)
        self.clear()
        self.root_element.draw()
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (10, 15, 300, 350)),
        ('c3B', (255, 255, 255, 0, 255, 0)))

    def on_keypress(self, symbol, modifiers):
        print symbol
        if symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self.cursorKey(symbol)

    def cursorKey(self, symbol):
        if symbol == key.UP:
            self.cursor_row -= 1
        elif symbol == key.DOWN:
            self.cursor_row += 1
        if symbol == key.LEFT:
            self.cursor_col -= 1
        elif symbol == key.RIGHT:
            self.cursor_col += 1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print 'The left mouse button was pressed.'
        #use reactive programming chains?
        #http://www.valuedlessons.com/2009/08/simple-rx-reactive-programming-in.html
        
        c,r = self.toCell(x,y)
        print "cell clicked:",c,r
        
    def toCell(self, x, y):
        """convert screen pixels to character space column and row"""
        return x/10,y/10

    def activeElement(self):
        """return the element under cursor"""
        pass
    
    
