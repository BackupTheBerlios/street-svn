#Module that controls information on all the users on CodeWorld
from CWModules.Server import LoginServer
    
Events.addCallbacks('net login', LoginServer.login)
Events.addCallbacks('net logout', LoginServer.logout)

Events.addCallbacks('quit', LoginServer.pwdDB.close)
