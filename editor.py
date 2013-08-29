__author__ = 'ankhmorporkian & sirdancealot'
from lemon_logger import LemonLogger
from element import *

import pyglet
from pyglet.gl import *

logger = LemonLogger()


class EditorWindow(pyglet.window.Window):
    """
    Editor class, creates an editing window for the lemon language.
    """

    def __init__(self, title='Lemon editor', font="monospace", size=18):
        super(EditorWindow, self).__init__(caption=title,
                                           resizable=True)
        self.setupGl()
        self.setFont()
        self.root_element = Element(root = True)

    def on_resize(self, width, height):
        super(EditorWindow, self).on_resize(width, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setupGl(self):
        glClearColor(1, 1, 1, 1)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(.5, .5, .5)
        glRectf(-.1, -.1, .1, .1)
        glColor3f(.05, .05, .05)
        glRectf(-.01, -.01, .01, .01)

    def setFont(self, font="monospace", size=18):
#        self.font = pygame.font.SysFont(font, size)
#        self.letter_width = self.font.render(" ",False,(0,0,0)).get_rect().width
#        self.letter_height = self.font.get_height()
	 pass
	
