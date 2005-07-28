#Package to handle events of any type.  The driving core of CodeWorld.

calls = {}

#Registers the passed callbacks for the specified event.
def addCallbacks(name, *callbacks):
    if(not calls.has_key(name)):
        calls[name] = [];
        
    for c in callbacks:
        calls[name].append(c)

#Unregisters the passed callbacks from the specified event.
def removeCallbacks(name, *callbacks):
    if(not calls.has_key(name)):
        return

    for c in callbacks:
        if(c in calls[name]):
            calls[name].remove(c)

    if(not len(calls[name])):
        del calls[name]

#Returns a list of callback functions for the specified event.
def getCallbacks(name):
    return (calls.has_key(name) and calls[name]) or None

#Registers all event/callback combinations from the passed hash.
def addGroups(groups):
    for key in groups.keys():
        addCallbacks(key, *groups[key]);

#Unregisters all event/callback combinations from the passed hash.
def removeGroups(groups):
    for key in groups.keys():
        removeCallbacks(key, *groups[key]);

#Returns the event/callback hash.
def getGroups():
    return calls;

#Handles an event immediately.
def do(name, *args, **keys):
    if(not calls.has_key(name)):
        return
    for callback in calls[name]:
        try:
            callback(*args, **keys)
        except Exception, exc:
            print "EXCEPTION: ", exc
    do(name + '_END', *args, **keys)
