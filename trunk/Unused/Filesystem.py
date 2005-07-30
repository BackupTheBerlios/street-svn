#Copyright (C) 2004-2005 Randall Leeds
#
#This file is part of The Street.
#
#The Street is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#The Street is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with The Street; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301

#Traverses The Street directory structure and builds a listing of files.
import os
import os.path

ignored = ['Server']
ignoref = ['streetserver.py']
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
    
