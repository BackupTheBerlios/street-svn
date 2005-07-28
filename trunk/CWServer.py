import glob
import signal
import sys

from CWModules import Events
from CWModules.Server import Core

def quit(signum, frame):
    Core.running = False

signal.signal(signal.SIGINT, quit)

print "Running startup scripts..."
startScripts = glob.glob('CWScripts/Startup/*.py')
startScripts += glob.glob('CWScripts/Server/Startup/*.py')
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
