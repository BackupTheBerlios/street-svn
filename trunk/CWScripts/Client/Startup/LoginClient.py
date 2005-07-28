#Sets up the callbacks for the Login module.

from CWModules import Events
from CWModules.Client import LoginClient

Events.addCallbacks('init_END', LoginClient.init)

Events.addCallbacks('net login', LoginClient.login)
Events.addCallbacks('net logout', LoginClient.logout)
