#Traverses the CodeWorld directory structure and builds a listing of files.
import os
import os.path

ignored = ['Server']
ignoref = ['CWServer.py']
cache = []

def build():
    for root, dirs, files in os.walk(''):
        if(root):
            fsys.append('dir %s\n' % root)
        for d in dirs:
            if(d in ignored):
                dirs.remove(d)
        for f in files:
            if(f not in ignoref and not f.endswith('.pyc')):
                fsys.append('%s\n' % os.path.join(root, f))
    
