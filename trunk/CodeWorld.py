import sys
import glob

from CWModules import Events

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

print 'Starting up CodeWorld client...'

print 'Setting up client output logging...'
clientLogger = Logger()

print 'Executing startup scripts...'
startScripts = glob.glob('CWScripts/Startup/*.py')
startScripts += glob.glob('CWScripts/Client/Startup/*.py')
startScripts += glob.glob('CWScripts/Client/User/Startup/*.py')
for script in startScripts:
    print '\t%s' % script
    execfile(script)

print 'Initializing the client...'
Events.do('init')
print 'CodeWorld client is up and running.'
Events.do('run')
Events.do('quit')
