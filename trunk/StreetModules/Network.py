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


#Modules that implements useful, inheritable sockets.

'''
NOTES:
TCP sockets buffer output and delivery is guaranteed.  The socket will
repeatedly try to send it's data on every flush until it gets written.
A TCP socket will mark itself as being ready to write data whenever the
buffer is not empty.  Calling TCPSocket.handleOutput will by default
call flush() which attempts to send the buffer again.  Override handleOutput
to change the functionality in a subclass, but make sure you always call
flush at the end.

UDP sockets are not guaranteed to deliver their data.
The write method of UDPSocket will NOT buffer the data and wait for
the socket to be flushed by handleOutput.
As a result, UDP sockets will never appear in wSocks.  Any writes to a UDP
socket will return immediately and data may or may not be sent.

It's recommended that for important data you always use TCP.

In reality, it's much faster if write just tries to send data and discards
it on failure.  However, by default, this module implements TCP sockets
which have a separation between their write and handleOutput methods.
If a TCP socket has buffered data, it will appear in the wSocks dictionary.

Of course, subclass any of the below classes to override any of the above.

NOTE ABOUT FILE-LIKE METHODS ON UDP SOCKETS:
Attempts to read will work, but will not give you the sender's address.
It's recommended that you only use read if you have connected the socket
to an explicit address or you don't care who the data came from.

Attempts to write on an unconnected socket will error.
Connect to an explicit address, that way send has a default destination.

Additionally, the file-transfer methods make heavy use of read/write.
For this reason, use them only on connected udp sockets, although using
them at all is not recommended.  UDP is too unreliable for file transfers.
The file-transfer methods are left in the parent class because technically
they should work, but probably not well.
'''

import socket

from errno import ECONNRESET, EWOULDBLOCK
from select import select
from string import find

from StreetModules import Checksum

_chunkSize = 8192
_tries = 5

serverAddress = ('192.168.2.110', 4242)

rSocks = {}
wSocks = {}

#Socket objects have an attribute fno, used to store the fileno at creation.
#This way, when the socket dies, we still have access to fno to remove it.
def addReadChannel(obj):
    rSocks[obj.fno] = obj

def delReadChannel(obj):
    if(obj.fno in rSocks):
        del rSocks[obj.fno]

def addWriteChannel(obj):
    wSocks[obj.fno] = obj

def delWriteChannel(obj):
    if(obj.fno in wSocks):
        del wSocks[obj.fno]

def multiplex(timeout = 0):
    if(rSocks or wSocks):
        return select(rSocks.values(), wSocks.values(), [], timeout)
    else:
        return ([], [], [])


class Socket(socket.socket):
    '''
    Constructor code borrowed in large part from socket.__init.
    Small change: don't alias functions if they're already assigned.
    This way, subclasses don't get their overriden method references mangled.
    '''
    
    def __init__(self, family, type, sock=None):
        if(sock):
            self._sock = sock._sock
        else:
            self._sock = socket._realsocket(family, type)
        
        self.fno = self.fileno()
        addReadChannel(self)
        
        if(not hasattr(self, 'send')): self.send = self._sock.send
        if(not hasattr(self, 'recv')): self.recv = self._sock.recv
        if(not hasattr(self, 'sendto')): self.sendto = self._sock.sendto
        if(not hasattr(self, 'recvfrom')): self.recvfrom = self._sock.recvfrom

    def recv(self, size, flags = 0):
        try:
            data = self._sock.recv(size, flags)
        except socket.error, (number, string):
            if(number == EWOULDBLOCK):
                return ''
            else:
                self.close()
                raise
        else:
            if(not data):
                self.close()
                raise socket.error(ECONNRESET, 'Connection reset by peer.')
            return data

    def recvfrom(self, size, flags = 0):
        try:
            result = self._sock.recvfrom(size, flags)
        except socket.error, (number, string):
                if(number == EWOULDBLOCK):
                    return ''
                else:
                    self.close()
                    raise
        else:
            if(not result):
                self.close()
                raise socket.error(ECONNRESET, 'Connection reset by peer.')
            return result

    def send(self, data):
        try:
            return self._sock.send(data)
        except socket.error, (number, string):
            if(number == EWOULDBLOCK):
                return 0
            else:
                self.close()
                raise

    def sendto(self, data, flags = 0, address = None):
        if(not address):
            return
        try:
            return self._sock.sendto(data, flags, address)
        except socket.error, (number, string):
            if(number == EWOULDBLOCK):
                return 0
            else:
                self.close()
                raise

    def read(self, size = _chunkSize):
        return self.recv(size)

    def readline(self, size = _chunkSize):
        line = self.recv(size, socket.MSG_PEEK)
        if(line):
            index = find(line, "\n")
            if(index < 0):
                return None
            return self.recv(index + 1)
        return ''

    def write(self, data):
        self.send(data)

    def flush(self):
        pass

    def recvfile(self, filename):
        self.handleInput = recvfilehelper(self.handleInput, filename).next
        addReadChannel(self)

    def sendfile(self, filename):
        self.handleOutput = sendfilehelper(self.handleOutput, filename).next
        addWriteChannel(self)

    def recvfilehelper(oldHandle, f):
        for i in range(_tries):
            if(isinstance(f, str)):
                #Open the file
                f = file(f, "wb")
            else:
                #Reset the file-like object the beginning
                f.reset()

            #Recieve the file size
            size = self.readline()
            while(not size):
                yield None
                size = self.readline()
            size = int(size[:-1])

            yield None

            #Receive the data
            while 1:
                data = self.read(size)
                size -= len(data)
                f.write(data)
                if(size <= 0):
                    break
                yield None
            f.close()

            #Send checksum back
            self.write(Checksum.md5sum(filename) + '\n')
            self.flush()

            #Wait for response
            response = self.readline()
            while(not response):
                yield None
                response = self.readline()
            response = response[:-1]

            #See if we're finished
            if(response == 'done'):
                break

        #Restore the original method
        self.handleInput = oldHandle
        yield 0

    def sendfilehelper(oldHandle, f):
        #Keep the checksum for future reference
        sum = Checksum.md5sum(filename)

        for i in range(_tries):
            if(isinstance(f, str)):
                #Open the file
                f = file(f, "rb")
            else:
                #Reset the file-like object the beginning
                f.reset()

            #Get the file size and send
            self.write(str(os.path.getsize(filename)) + '\n')
            self.flush(noremove = True)

            yield None

            #Get the file data and send
            data = f.read(_chunkSize)
            while(data):
                self.write(data)
                while(self.wBuf):
                    self.flush(noremove = True)
                    yield None
                data = f.read(_chunkSize)
            f.close()

            ##Wait for checksum
            
            #Mark this socket not waiting to read, but have us wake on input
            delWriteChannel(self)
            temp = self.handleInput
            self.handleInput = self.handleOutput

            #Actually receive the checksum
            check = self.readline()
            while(not check):
                yield None
                check = self.readline()

            #Restore the socket's state
            self.handleInput = temp
            addWriteChannel(self)

            #Send response
            if(check[:-1] == sum):
                self.write('done\n')
                self.flush()
                break
            else:
                self.write('retr\n')
                self.flush(noremove = True)
                
        #Restore the original method
        sock.handleOutput = oldHandle
        yield 0

    def close(self):
        delReadChannel(self)
        delWriteChannel(self)
        self._sock.close()

    #Stubs. Functional child classes should implement these.
    def handleOutput(self):
        pass

    def handleInput(self):
        pass

#Implements an inheritance-friendly TCPSocket with file operations.
class TCPSocket(Socket):
    def __init__(self, sock=None):
        Socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM, sock)
        try:
            self.getpeername()
        except:
            pass #Socket not connected yet.
        else:
            self.settimeout(0)

        self.wBuf = ''

    #Override the default.  Buffer the data, then wait for handleOutput().
    def write(self, data):
        addWriteChannel(self)
        self.wBuf += data

    def flush(self, noremove = False):
        if(not self.wBuf):
            return
        try:
            result = self.send(self.wBuf[:_chunkSize])
        except socket.error:
            raise
        else:
            self.wBuf = self.wBuf[result:]
            if(not (self.wBuf or noremove)):
                delWriteChannel(self)
    

    def connect(self, address):
        self._sock.connect(address)
        self.settimeout(0)

    #Default handle methods.
    def handleInput(self):
        self.read()

    def handleOutput(self):
        self.flush()

#Implements a simple, error-handling, inheritance-friendly UDP socket.
class UDPSocket(Socket):
    def __init__(self, port=0, sock=None):
        Socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM, sock)
        try:
            self.getsockname()
        except:
            self.bind(('', port))
        self.settimeout(0)

    def handleOutput(self):
        pass
    
    def handleInput(self):
        self.read()
        
