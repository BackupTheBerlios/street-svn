#Controls the core event processing, i.e. posting the user-level events
#in response to system events.

import sys
import time

import pygame

import pyui
from pyui.desktop import getRenderer
from pyui.desktop import getDesktop

from OpenGL.GL import *
from OpenGL.GLU import *

from CWModules import Events, Network

width = 1024
height = 768

user = None

def drawFPS():
    global lasttime, frame, fps
    try:
        now = time.time()
        if(now - lasttime > 1):
            fps = frame
            lasttime = now
            frame = 0
        else:
            frame += 1
    except NameError:
        lasttime = time.time()
        frame = 1
        fps = 0
        return

    getRenderer().setup2D()
    #glTranslatef(0.0, 0.0, -1.0)
    getRenderer().drawText(str(fps), (20, 20), pyui.colors.white)
    getRenderer().teardown2D()

def render():
    getRenderer().clear()
    Events.do('render')
    drawFPS()

def update():
    getDesktop().draw()
    getDesktop().update()
    
    r, w, e = Network.multiplex()
    for sock in r:
        try:
            sock.handleInput()
        except Exception, exc:
            print "Unhandled exception:", exc
    for sock in w:
        sock.handleOutput()
    for sock in e:
        sock.close()

def keyDown(event):
    Events.do('keyDown', event)
    if(event.key == 27):
        Events.do('quit')
        return 1
    return 0

def init():
    pyui.init(width, height, 'p3d', fullscreen = 1, title = "CodeWorld")
    getRenderer().setBackMethod(render)
    getDesktop().registerHandler(pyui.locals.KEYDOWN, keyDown)
    pygame.key.set_repeat(500, 30)
    
    initGL()

def initGL():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width/height, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def run():
    pyui.run(update)

def quit():
    pyui.quit()
