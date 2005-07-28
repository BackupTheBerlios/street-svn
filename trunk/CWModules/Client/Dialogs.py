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
