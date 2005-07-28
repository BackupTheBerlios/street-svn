#Defines a console - a display that shows stdout output.  Like a quake console.
import sys

import pyui
from pyui.desktop import getDesktop
from pyui.dialogs import LineDisplay
from pyui.widgets import Window

from CWModules import Events

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
