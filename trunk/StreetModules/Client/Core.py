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

#Controls the core event processing, i.e. posting the user-level events
#in response to system events.

import sys
import time
import os

try:
	from pyogre import ogre
	from pyogre import cegui
except ImportError, e:
	raise ImportError, e.__str__() + \
		'\nMake sure you have installed both OGRE and PyOGRE and CEGUI support ' \
			+ 'is enabled.\nSee the webpage for additional support.'

from StreetModules import Events, Network

root = None
window = None

input = None
gui = None
system = None

scene = None
camera = None
viewport = None

user = None

done = False

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
	global root
	root = ogre.Root('plugins.cfg', 'display.cfg', "ogre.log")
	initPlugins()
	initDisplay()
	initResources()
	initScene()
	initGUI()
	initInput()

def initPlugins():
	global root
	plugins = ['RenderSystem_Direct3D9',
		'RenderSystem_GL',
		'Plugin_ParticleFX',
		'Plugin_BSPSceneManager',
		'Plugin_OctreeSceneManager',
		'Plugin_CgProgramManager']
	for plugin in plugins:
		try:
			root.loadPlugin(plugin)
		except:
			pass

def initDisplay():
	global root, window, scene, camera, viewport
	root.restoreConfig()
	if(not root.renderSystem):
		try:
			root.renderSystem = root.getAvailableRenderers()[0]
		except:
			print "No useable rendering subsystems found.  Check your OGRE installaiton."
	window = root.initialise(True, "The Street")

def initResources():
	global root
	for path, dirs, files in os.walk('StreetData/Client'):
		if 'CVS' in dirs:
			dirs.remove('CVS')
		if '.svn' in dirs:
			dirs.remove('.svn')
		ogre.ResourceGroupManager.getSingleton().addResourceLocation(path, \
			'FileSystem', 'General')
	ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()	

def initScene():
	global root, window, scene, camera, viewport
	scene = root.getSceneManager(ogre.ST_GENERIC)
	camera = scene.createCamera("DefaultCam")
	camera.position = (0,0,0)
	camera.lookAt = (0,0,-1)
	camera.nearClipDistance = 1
	viewport = window.addViewport(camera)
	viewport.backgroundColour = (0,0,0)

def initGUI():
	global root, window, gui, system
	gui = cegui.OgreCEGUIRenderer(window)
	system = cegui.System(gui)
	
	# create font
	cegui.FontManager.getSingleton().createFont("tahoma-12.font")
	# Load Default CEGUI Window
	sheet = cegui.WindowManager.getSingleton().createWindow("DefaultWindow", "root_wnd")
	
	cegui.SchemeManager.getSingleton().loadScheme("TaharezLook.scheme")

def initInput():
	global root, window, input
	input = ogre.PlatformManager.getSingleton().createInputReader()
	input.initialise(window)

def initGL():
	global root
	
	#glClearColor(0.0, 0.0, 0.0, 0.0)
	#glClearDepth(1.0)
	#glDepthFunc(GL_LEQUAL)
	#glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

	#glEnable(GL_DEPTH_TEST)
	#glMatrixMode(GL_PROJECTION)
	#glLoadIdentity()
	#gluPerspective(45.0, width/height, 0.1, 100)

	#glMatrixMode(GL_MODELVIEW)
	#glLoadIdentity()

def run():
	global root, input, done
	while(not done):
		input.capture()
		if(input.isKeyDown(ogre.KC_ESCAPE)):
			Events.do('quit')
		root.renderOneFrame()

def quit():
	global done
	done = True

def cleanup():
	global root
	root.saveConfig()
	root.detachRenderTarget(root.getRenderTarget("The Street"))
