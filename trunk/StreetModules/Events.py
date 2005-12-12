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

#Package to handle events of any type.  The driving core of The Street.

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
