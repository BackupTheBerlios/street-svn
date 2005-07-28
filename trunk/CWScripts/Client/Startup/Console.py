#Initializes one quake-like console window.
from CWModules import Events
from CWModules.Client import Console

Events.addCallbacks('init_END', Console.init)
Events.addCallbacks('showConsole', Console.showConsole)
Events.addCallbacks('hideConsole', Console.hideConsole)
