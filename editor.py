__author__ = 'ankhmorporkian & sirdancealot'
import random

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

from lemon_logger import LemonLogger
from element import *
from clock import Clock


logger = LemonLogger()


class EditorWindow(pyglet.window.Window):
    """
    Editor class, creates an editing window for the lemon language.
    """

    def __init__(self, title='Lemon editor', font_name="monospace", font_size=18):
        super(EditorWindow, self).__init__(caption=title,
                                           resizable=True)
        self.setupGl()
        self.font = Font(font_name, font_size)
        self.root_element = Element(root=True)
        Clock(self.root_element)
        self.root_element.setPosition(0, 0)
        self.keys = key.KeyStateHandler()
        for x in range(20):
            TextElement(self.root_element, text='Test element ' + str(x), font_name="monospace",
                        font_size=random.randint(6, 20))
        self.x, self.y = self.get_location()
        self.y_offset = 0
        self.cursor_row = 0
        self.cursor_col = 0

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
        self.key_handler()
        self.clear()
        self.root_element.draw(y_height=0, y_offset=int(self._height + self.cursor_row))
        #pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #('v2i', (10, 15, 300, 350)),
        #('c3B', (255, 255, 255, 0, 255, 0)))

    def on_key_press(self, symbol, modifiers):
        self.push_handlers(self.keys)

    def on_key_release(self, symbol, modifiers):
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

    def key_handler(self):
        #logger.info("key-handler")
        self.push_handlers(self.keys)
        for k in self.keys:
            logger.info(k)
            if k in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
                self.cursorKey(k)

    def cursorKey(self, symbol):
        if symbol == key.UP:
            self.cursor_row -= 10
        elif symbol == key.DOWN:
            self.cursor_row += 10
        if symbol == key.LEFT:
            self.cursor_col -= 1
        elif symbol == key.RIGHT:
            self.cursor_col += 1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            logger.info('The left mouse button was pressed.')
            #use reactive programming chains?
        #http://www.valuedlessons.com/2009/08/simple-rx-reactive-programming-in.html

        c, r = self.toCell(x, y)
        logger.info("Cell clicked:", c, r)
        logger.info("Clicked:", x, y)

    def toCell(self, x, y):
        """convert screen pixels to character space column and row"""
        return x / 10, y / 10

    def activeElement(self):
        """return the element under cursor"""
        pass
    
    
