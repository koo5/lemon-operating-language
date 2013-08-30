__author__ = 'ankhmorporkian & sirdancealot'

from string import ascii_lowercase

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
        #self.keys = key.KeyStateHandler()
        for x in range(20):
            TextElement(self.root_element, text='Test element ' + str(x), font_name="monospace", )
        ButtonElement(self.root_element)
        self.x, self.y = self.get_location()
        self.y_offset = 0
        self.cursor_row = 0
        self.cursor_col = 0
        self.active_element = self.root_element.getChild(0)
        self.caret_visible = True
        pyglet.clock.schedule_interval(self.blink, .75)

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
        self.root_element.draw(y_height=0, y_offset=int(self._height + self.cursor_row))
        if self.cursor_col > self.active_element.getLen():
            self.cursor_col = self.active_element.getLen()
        self.caret()

    def blink(self, dt):
        self.caret_visible = not self.caret_visible
        #pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #('v2i', (10, 15, 300, 350)),
        #('c3B', (255, 255, 255, 0, 255, 0)))

    def caret(self):
        active_x_offset = self.cursor_col * self.active_element.getLetterWidth()
        active_x = self.active_element.getX() + active_x_offset
        active_y = self.active_element.getY()
        active_height = self.active_element.getHeight()
        active_width = self.active_element.getWidth()
        if self.caret_visible: Rectangle(active_x, active_y + active_height, active_x + 1, active_y)

    def on_key_press(self, symbol, modifiers):
        #logger.info("key-handler")
        if symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            self.cursorKey(symbol)
        else:
            self.type_letter(symbol)

    def type_letter(self, k):
        keycodes = dict(zip([key.A, key.B, key.C, key.D, key.E, key.F, key.G, key.H, key.I, key.J, key.K, key.L
                                , key.M, key.N, key.O, key.P, key.Q, key.R, key.S, key.T, key.U, key.V, key.W, key.X,
                             key.Y, key.Z], ascii_lowercase))

        if k in keycodes:
            self.addLetter(keycodes[k])
        if k == key.BACKSPACE:
            self.backspaceLetter()
        if k == key.SPACE:
            self.addLetter(' ')
        if k == key.DELETE:
            self.delLetter()
        if k == key.HOME:
            self.cursor_col = 0
        if k == key.END:
            self.cursor_col = self.active_element.getLen()

    def addLetter(self, letter):
        self.active_element.addText(letter, self.cursor_col)
        self.cursor_col += 1

    def backspaceLetter(self):
        if self.active_element.popText(self.cursor_col - 1):
            self.cursor_col -= 1

    def delLetter(self):
        self.active_element.popText(self.cursor_col)

    def cursorKey(self, symbol):
        if symbol == key.UP:
            self.cursor_row -= 1
        elif symbol == key.DOWN:
            self.cursor_row += 1
        elif symbol == key.LEFT:
            self.cursor_col -= 1
        elif symbol == key.RIGHT:
            self.cursor_col += 1
        self.updateActiveElement()

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

    def updateActiveElement(self):
        self.active_element = self.root_element.getChild(self.cursor_row)
    
