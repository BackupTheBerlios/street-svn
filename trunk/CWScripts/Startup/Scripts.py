#Sets up events for the Scripts module.

from CWModules import Scripts, Events

Events.addCallbacks('runScript', Scripts.run)
