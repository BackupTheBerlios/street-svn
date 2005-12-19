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

#Module to load configuration files
#Converts an instance of OGRE's ConfigFile into a useful python dictionary

from pyogre.ogre import ConfigFile

class Config(dict):
	def __init__(self, filename):
		c = ConfigFile()
		try:
			c.loadFromFile(filename)
		except:
			pass #Silently fail if the file doesn't exist

		for section, key, val in c.values:
			self.setdefault(section, {})
			self[section][key] = val
	
	def save(self, filename):
		try:
			f = open(filename, 'w')
		except:
			return False

		for section in self:
			f.write('[' + section + ']\n')
			for key, val in self[section].items():
				f.write(key + '=' + val + '\n')

		f.close()
		return True
