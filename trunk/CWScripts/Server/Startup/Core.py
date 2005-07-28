#Sets up the Core module.

from CWModules import Events
from CWModules.Server import Core

Events.addCallbacks('init', Core.init)
Events.addCallbacks('run', Core.run)
Events.addCallbacks('quit', Core.quit)
