#Sets up a console window for testing

import code
import sys
import string

import pyui
from pyui.dialogs import Console

import pygame

from StreetModules.Client import ScreenUtils
        
class RealConsole(Console):
    def __init__(self, x, y, w, h, callback = None):
        Console.__init__(self, x, y, w, h)

        self.interp = code.InteractiveInterpreter()
        self.buffer = ""
        self.tabature = 0

        self.outputBox.addLine(">")

    def _pyuiOutput(self, event):
        if(not self.output):
            return 1
        if(not self.output.getLines()):
            return 1
        
        out = self.output.lines.pop(0)
        
        line, color = self.outputBox.displayLines.pop()
        if(line and line[len(line)-1] == '|'):
            line = line[:-1]
        line += out
        self.outputBox.addDisplayLine(line, color)
        
        line, color = self.outputBox.lines.pop()
        if(line and line[len(line)-1] == '|'):
            line = line[:-1]
        line += out
        self.outputBox.lines.append((line, color))
        pyui.dialogs.Console._pyuiOutput(self, event)
        
        return 1

    def _pyuiGo(self, sender):
        command = self.inputBox.text
        self.output.beginCapture()
        if(not command):
            self.outputBox.addLine("|")
        if(command == '.'):
            self.tabature -= 1
            if(self.tabature < 0): self.tabature = 0
            self.outputBox.addLine("|")
            if(self.buffer):
                print ' ' * 4 * self.tabature + '|',
            else:
                print '>',
        else:
            self.buffer += "\n" + " " * 4 * self.tabature + "%s" % command
            print command
            if(self.interp.runsource(self.buffer)):
                if(command and command[len(command)-1] == ':'):
                    self.tabature += 1
                if(not command and self.tabature == 0):
                    self.buffer = ""
                    print ">",
                else:
                    print ' ' * 4 * self.tabature + '|',
            else:
                print ">",
                self.buffer = ""
                self.tabature = 0
        self.output.endCapture()
        

def init():
    x, y = ScreenUtils.center(640, 480)
    RealConsole(x, y, 640, 480)
    #pyui.dialogs.Console(x, y, 640, 480)
