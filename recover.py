import struct

CHUNK = 1024 * 1024 * 100 #process 100 megs at a time.

TOPLEVEL = ['skip', 'wide', 'mdat', 'moov']

def look(data):
    for tl in TOPLEVEL:
        if tl in data:
            print "LOOK:",tl
            yield tl
def extract(f,tag,position):
    print "EXTRACT:",tag+"@%d"%position
    loc = f.tell()
    f.seek(position)
    dat = f.read(4)
    size = struct.unpack('>I',dat)[0]
    assert tag == f.read(4)
    f.seek(-8,1)
    try:
        dat = f.read(size)
    except:
        print "  EXTRACT FAILED"
        dat = ''
    f.seek(loc)
    return dat

def process_data(f):
    #hack to correctly account for file position since we always keep 8 bytes in the buffer
    buffer = "00000000" 
    #Keep tract of the file position relative to the beginning of the buffer
    POS = -CHUNK
    # store any chucks that we find.
    found = {}
    while 1:
        buffer += disk.read(CHUNK)
        if len(buffer) == 8:
            break
        POS += CHUNK
        for tag in look(buffer):
            pos = POS + buffer.index(tag) - 4 - 8
            dat = extract(disk, tag, pos)
            found[tag+'@%d'%pos] = dat
        buffer = buffer[-8:]
    return found

if __name__=='__main__':
    import sys
    if len(sys.argv) == 2:
        disk = open(sys.argv[1],'rb')
        found = process_data(disk)
    else:
        print "Usage: python recover.py /path/to/disk.dat"

