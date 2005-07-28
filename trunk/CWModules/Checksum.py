#Module for MD5 checksumming.

import md5

def md5sum(filename):
    f = file(filename, 'rb')
    m = md5.new()
    while 1:
        buf = f.read(8096)
        if(not buf):
            break
        m.update(buf)
    return m.hexdigest()
