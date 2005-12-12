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

#Provides a small command bar at the bottom of the screen

import string

import pyui
from pyui.desktop import getDesktop
from pyui.dialogs import LineDisplay
from pyui.widgets import Window, Edit

from StreetModules import Events

class CommandLine(Window):
    def __init__(self):
        Window.__init__(self, 0, getDesktop().height-24, getDesktop().width, 24, topmost = 1)
        self.setLayout(pyui.layouts.BorderLayoutManager())
        
        self.command = Edit("Enter commands here.", 255, self.enter)
        self.addChild(self.command, pyui.locals.CENTER)
        self.pack()
        
    def enter(self, widget):
        if(self.command.text != ''):
            s = string.split(self.command.text, maxsplit = 1)
            self.command.setText('')
            self.setDirty()
            if(len(s) > 1):
                Events.do('command-' + s[0], s[1])
            else:
                Events.do('command-' + s[0])
            

def init():
    CommandLine()
    