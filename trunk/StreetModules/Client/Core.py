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

from StreetModules import Config, Events, Network

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
	root = ogre.Root()
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
	print 'Loading OGRE plugins...'
	for plugin in plugins:
		try:
			root.loadPlugin(plugin)
		except:
			pass

def initDisplay():
	global root, window
	
	print 'Setting up the display...'
	displayDefaults = {
		'RenderSystem': root.getAvailableRenderers()[0].name,
		'Width': '800',
		'Height': '600',
		'Fullscreen': 'False'
	}
	displayCfg = Config.Config('street.ini')
	displayOpts = displayCfg.get('Display', {})
	for key, val in displayDefaults.items():
		displayOpts.setdefault(key, val)
	displayCfg['Display'] = displayOpts
	displayCfg.save('street.ini')

	for renderer in root.getAvailableRenderers():
		if(renderer.name == displayOpts['RenderSystem']):
			root.renderSystem = renderer

	if(not root.renderSystem):
		raise Error, "No useable rendering subsystems found.  Check your OGRE installaiton."
	else:
		window = root.createRenderWindow('The Street', \
			int(displayOpts['Width']), \
			int(displayOpts['Height']), \
			displayOpts['Fullscreen'] == 'True'
		)

def initResources():
	global root
	print 'Loading resources...'
	for path, dirs, files in os.walk('StreetData/Client'):
		if '.svn' in dirs:
			dirs.remove('.svn')
		root.addResourceLocation(path, 'FileSystem', 'General')
		#ogre.ResourceGroupManager.getSingleton().addResourceLocation(path, \
		#	'FileSystem', 'General')
	ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()	

def initScene():
	global root, window, scene, camera, viewport
	print 'Setting up the scene, camera, and viewport...'
	scene = root.getSceneManager(ogre.ST_GENERIC)
	camera = scene.createCamera("DefaultCam")
	camera.position = (0,0,0)
	camera.lookAt = (0,0,-1)
	camera.nearClipDistance = 1
	viewport = window.addViewport(camera)
	viewport.backgroundColour = (1,0,0)

def initGUI():
	global root, window, gui, system
	print 'Initialising GUI system...'
	gui = cegui.OgreCEGUIRenderer(window)
	system = cegui.System(gui)
	cegui.Logger.getSingleton().loggingLevel = cegui.Insane
	
	print 'Setting up GUI...'
	cegui.FontManager.getSingleton().createFont("tahoma-12.font")
	cegui.SchemeManager.getSingleton().loadScheme("TaharezLook.scheme")
	gui.defaultMouseCursor = ("TaharezLook", "MouseArrow")
	
	sheet = cegui.WindowManager.getSingleton().createWindow("DefaultWindow", "root_wnd")
	system.GUISheet = sheet
	sheet.visible = True
	
	frame = cegui.WindowManager.getSingleton().createWindow("TaharezLook/FrameWindow", "Frame 1")
	frame.frameEnabled = True
	frame.size = cegui.Size(0.4, 0.4)
	frame.position = cegui.Vector2(0.1, 0.1)
	frame.visible = True
	frame.alpha = 0.5
	frame.text = 'Test'
	sheet.addChildWindow(frame)

def initInput():
	global root, window, input, events
	print 'Initialising input system...'
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
	global root, window, system, input, events, done
	cm = ogre.ControllerManager()
	while(not done):
		input.capture()
		if(input.isKeyDown(ogre.KC_ESCAPE)):
			Events.do('quit')
		'''evt = events.pop()
		while(evt):
			print evt.mId
			evt = events.pop()
		if(input.mouseRelativeX or input.mouseRelativeY):
			cegui.System.getSingleton().injectMouseMove( \
				input.mouseRelativeX * window.width, \
				input.mouseRelativeY * window.height)'''
		root.renderOneFrame()
		#system.renderGUI()

def keyDown(evt):
	cegui.System.getSingleton().injectKeyDown(evt.key)
	cegui.System.getSingleton().injectChar(evt.keyChar)
	Events.do('keyDown', evt.key)
	print 'Generated keyDown event with key:' + evt.key

def keyUp(evt):
	cegui.System.getSingleton().injectKeyUp(evt.key)
	Events.do('keyUp', evt.key)

def mouseMoved(evt):
	global window
	x = evt.relX * window.width
	y = evt.relY * window.height
	cegui.System.getSingleton().injectMouseMove(x, y)
	Events.do('mouseMove', x, y)

def quit():
	global done
	done = True

def cleanup():
	global root
	root.detachRenderTarget(root.getRenderTarget("The Street"))
