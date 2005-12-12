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

import glob
import signal
import sys

from StreetModules import Events
from StreetModules.Server import Core

def quit(signum, frame):
	Core.running = False

signal.signal(signal.SIGINT, quit)

print "Running startup scripts..."
startScripts = glob.glob('StreetScripts/Startup/*.py')
startScripts += glob.glob('StreetScripts/Server/Startup/*.py')
for script in startScripts:
	print script
	execfile(script)

print "Running initialization events..."
Events.do('init')
print "Server is up and running!"
Events.do('run')
print "Server shutting down..."
print "Running shutdown events..."
Events.do('quit')
print "Server is offline."
