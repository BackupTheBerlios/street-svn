#Sets up a console window for testing.

from CWModules import Events
from CWModules.Client.User import RealConsole

Events.addCallbacks('start', RealConsole.init)
