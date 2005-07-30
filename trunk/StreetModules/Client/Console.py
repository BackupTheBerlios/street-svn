#Copyright (C) 2004-2005 Randall Leeds
#
#This file is part of The Street.
#
#The Street is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#The Street is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with The Street; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301

#Defines a console - a display that shows stdout output.  Like a quake console.
import sys

import pyui
from pyui.desktop import getDesktop
from pyui.dialogs import LineDisplay
from pyui.widgets import Window

from StreetModules import Events

console = None

class Console(Window):
    def __init__(self):
        Window.__init__(self, 0, 0, getDesktop().width, \
                        getDesktop().height/4, topmost = 1)
        self.setLayout(pyui.layouts.BorderLayoutManager())
        self.outputBox = LineDisplay()
        self.addChild(self.outputBox, pyui.locals.CENTER)
        self.pack()

	Events.addCallbacks('keyDown', self.keyDown)
	
        self.oldout = sys.stdout
        sys.stdout = self

    def write(self, text):
        self.outputBox.addLine(text)
        self.oldout.write(text)

    def keyDown(self, event):
        if(event.key < 256 and chr(event.key) == '`'):
            if(self.show == 1):
                hideConsole()
            else:
                showConsole()
            return 1
        return 0

def init():
    global console
    if(not console):
        console = Console()
        hideConsole()

def showConsole():
    global console
    console.setShow(1)

def hideConsole():
    global console
    console.setShow(0)
