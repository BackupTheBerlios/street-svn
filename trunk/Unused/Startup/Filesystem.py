#Traverses the CodeWorld directory structure and builds a listing of files.
from CWModules import Events
from CWModules.Server import Filesystem

Events.add('net update', lambda user: user.sendfile(

filesystem = []

ignored = ['Server']
ignoref = ['CWServer.py']

def construct():
    for root, dirs, files in os.walk(''):
        if(root):
            filesystem.append('dir %s\n' % root)
        for d in dirs:
            if(d in ingored):
                dirs.remove(d)
        for f in files:
            if(f not in ignoref and not f.endswith('.pyc')):
                filesystem.append('%s\n' % os.path.join(root, f))
