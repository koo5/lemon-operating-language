#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pyglet
from datetime import datetime

from element import Element


class Clock(Element):

    def __init__(self, parent):
        super(Clock, self).__init__(self, parent)

        self.label = pyglet.text.Label(self.getText(), 'monospace',
                font_size=18, x=0, y=0)

        # pyglet.clock.schedule_interval(self.dummy, 1)  # Bad mojo at the moment.

    def dummy(self, deltaT):
        pass

    def getText(self):
        return str(datetime.now())

    def draw(self):
        self.label.text = self.getText()
        self.label.draw()
