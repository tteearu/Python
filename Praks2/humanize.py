
import os
from datetime import datetime

def humanize(bytes):
    if bytes < 1024:
        return  "%.2f B" % bytes
    elif bytes < 1024 ** 2:
        return "%.2f kB" % (bytes / 1024)
    elif bytes < 1024 ** 3:
        return "%.2f MB" % (bytes / 1024 ** 2)
    else:
        return "%.2f GB" % (bytes / 1024 ** 3)

files = []

for filename in os.listdir("."):
    mode, inode, devide, nlink, uid, gid, size, atime, mtime, ctime = os.stat(filename)
    files.append((filename, datetime.fromtimestamp(mtime), size))

print

files.sort(key = lambda(filename, dt, size):dt)
for filename, dt, size in files:
    print filename, dt, humanize(size)
    
print
print "Newest file is: ", files[-1][0]
print "Oldest file is: ", files[0][0]
print
