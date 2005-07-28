#Initializes the User module
from CWModules import Events, User

Events.addCallbacks('net bindUDP', User.bindUDP)
