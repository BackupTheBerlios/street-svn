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

#Module to install, run, and maintain the CodeWorld scripts.

import os

directories = ['StreetScripts']

def run(name):
    for d in directories:
        print d + name
        if(os.path.exists(d + '/' + name + '.py')):
            execfile(d + '/' + name + '.py')
            break

def install(path):
    try:
        directories.index(path)
    except:
        directories.append(path)

def uninstall(path):
    try:
        directories.remove(path)
    except:
        pass

