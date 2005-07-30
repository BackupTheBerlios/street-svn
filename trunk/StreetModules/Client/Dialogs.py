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

#Module that defines some useful dialog window types.

import pyui
from pyui.dialogs import Dialog, LineDisplay

class MultiLineDialog(Dialog):
    def __init__(self, x = -1, y = -1, w = 300, h = 200, title = None):
        Dialog.__init__(self, x, y, w, h, title)
        self.setLayout(pyui.layouts.BorderLayoutManager())

        self.lines = LineDisplay()
        self.addChild(self.lines, pyui.locals.CENTER)

        self.pack()

        self.oldout = sys.stdout
        self.oldin = sys.stdin

    def addLine(self, text):
        self.lines.addLine(text)
