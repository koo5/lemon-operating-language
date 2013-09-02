__author__ = 'ankhmorporkian & sirdancealot'

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

from lemon_logger import LemonLogger
from element import *
from clock import Clock


logger = LemonLogger()


class EditorWindow(pyglet.window.Window):
    """
    EditorWindow class, creates an editing window for the lemon language.
    """

    def __init__(self, title='Lemon editor', font_name="monospace", font_size=18):
        super(EditorWindow, self).__init__(caption=title,
                                           resizable=True)
        self.set_icon(pyglet.image.load("icon32x32.png"))
        self.setupGl()
        self.font = Font(font_name, font_size)
        self.root_element = Element(root=True)
        Clock(self.root_element)
        self.root_element.setPosition(0, 0)
        #self.keys = key.KeyStateHandler()
        tm = TemplateManager()
        templates = ["for", "if", "while", "for2", "while2", "define <<a>> as <<b>>", "when",
                     "then"]  # Dumb starter elements
        for name in templates:
            tm.addTemplate(Template(name))
        for x in range(20):
            a = TextElement(self.root_element, text='', font_name="monospace", )
            a.template_manager = tm
        self.x, self.y = self.get_location()
        self.y_offset = 0
        self.cursor_row = 0
        self.cursor_col = 0
        self.active_element = self.root_element.getChild(0)
        self.caret_visible = True
        pyglet.clock.schedule_interval(self.blink, .75)

    def toggleFullscreen(self):
        self.setFullscreen(not self.fullscreen)

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
        self.drawCaret()

    #        logger.info("on_draw")


    def blink(self, dt):
        self.caret_visible = not self.caret_visible
        #pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #('v2i', (10, 15, 300, 350)),
        #('c3B', (255, 255, 255, 0, 255, 0))) q

    def drawCaret(self):
        active_x_offset = self.cursor_col * self.active_element.getLetterWidth()
        active_x = self.active_element.getX() + active_x_offset
        active_y = self.active_element.getY()
        active_height = self.active_element.getHeight()
        active_width = self.active_element.getWidth()
        if self.caret_visible:
            glColor3f(1, 1, 1)
        else:
            glColor3f(0.2, 0.2, 0.2)
        Rectangle(active_x, active_y + active_height, active_x + 1, active_y)

    def on_text_motion(self, k):
        #logger.info("key-handler")
        if k == key.BACKSPACE:
            self.backspaceLetter()
        if k == key.DELETE:
            self.delLetter()
        if k == key.HOME:
            self.cursor_col = 0
        if k == key.END:
            self.cursor_col = self.active_element.getLen()
        if k == key.UP:
            self.cursor_row -= 1
        if k == key.DOWN:
            self.cursor_row += 1
        if k == key.LEFT:
            self.cursor_col -= 1
        if k == key.RIGHT:
            self.cursor_col += 1
        self.updateActiveElement()
        self.pauseCaret()

    def on_text(self, text):
        self.cursor_col += self.active_element.addText(text, self.cursor_col)

    def backspaceLetter(self):
        if self.active_element.popText(self.cursor_col - 1):
            self.cursor_col -= 1

    def delLetter(self):
        self.active_element.popText(self.cursor_col)


    def pauseCaret(self):
        """postpones caret blink (when moving, editing)"""
        self.caret_visible = True
        pyglet.clock.unschedule(self.blink)
        pyglet.clock.schedule_interval(self.blink, .75)

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