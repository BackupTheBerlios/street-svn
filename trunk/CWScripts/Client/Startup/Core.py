#Initialize core event callbacks at startup time.

from CWModules import Events
from CWModules.Client import Core

Events.addCallbacks('init', Core.init)
Events.addCallbacks('run', Core.run)
Events.addCallbacks('quit', Core.quit)


