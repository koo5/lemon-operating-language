__author__ = 'ankhmorporkian'
from LemonLogger import LemonLogger
import pygame
from Element import *

logger = LemonLogger()

class Editor(object):
    """
    Editor class, creates an editing window for the lemon language.
    """
    def __init__(self, title='Lemon editor', width=640, height=480, font="monospace", size=18):
        pygame.init()
        pygame.display.set_caption(title)
        self.setFont(font, size)
        self.window = pygame.display.set_mode((width, height))
        self.screen = pygame.display.get_surface()
        self.root_element = Element()

    def setFont(self, font="monospace", size=18):
        self.font = pygame.font.SysFont(font, size)
        self.letter_width = self.font.render(" ",False,(0,0,0)).get_rect().width
        self.letter_height = self.font.get_height()

    def renderLoop(self):
        self.root_element.render()

