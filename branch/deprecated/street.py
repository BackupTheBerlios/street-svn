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

import sys
import glob

from StreetModules import Events

class Logger:
    def __init__(self):
        self.oldout = sys.stdout
        sys.stdout = self
        self.logFile = file('clientlog.txt', 'w')
    
    def write(self, text):
        self.oldout.write(text)
        self.logFile.write(text)
	self.logFile.flush()
        
    def __del__(self):
        self.logFile.close()

print 'Starting up The Street client...'

print 'Setting up client output logging...'
clientLogger = Logger()

print 'Executing startup scripts...'
startScripts = glob.glob('StreetScripts/Startup/*.py')
startScripts += glob.glob('StreetScripts/Client/Startup/*.py')
startScripts += glob.glob('StreetScripts/Client/User/Startup/*.py')
for script in startScripts:
    print '\t%s' % script
    execfile(script)

print 'Initializing the client...'
Events.do('init')
print 'The Street client is up and running.'
Events.do('run')
print "Shutting down the client..."
print "Running shutdown events..."
Events.do('quit')
print "Client offline."