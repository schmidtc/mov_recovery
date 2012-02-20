import struct
fname = 'disk.dat'
disk = open(fname,'rb')

CHUNK = 1024 * 1024 * 100

moov = 0
mdat = 0
ftyp = 0
buffer = "00000000"
POS = -CHUNK
c= 0

TOPLEVEL = ['skip', 'wide', 'mdat', 'moov']

def look(data):
    for tl in TOPLEVEL:
        if tl in data:
            print "LOOK:",tl
            yield tl
def extract(f,tag,position):
    print "EXTRACT:",tag, position
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

found = {}

while 1:
    #print "loop",c
    c+=1
    buffer += disk.read(CHUNK)
    if len(buffer) == 8:
        break
    POS += CHUNK
    for tag in look(buffer):
        pos = POS + buffer.index(tag) - 4 - 8
        dat = extract(disk, tag, pos)
        found[tag+'@%d'%pos] = dat
    buffer = buffer[-8:]

def writeMovie(mdat):
    o = open('found.mov','wb')
    o.write(found['skip@58643968'])
    o.write(found['wide@61437816'])
    o.write(found['mdat@61437824'])
    o.write(found['moov@65087363'])
def writeBack(c = 1, end = 1428428969):
    o = open('back.mov','wb')
    o.write(found['skip@58643968'])
    o.write(found['wide@61437816'])
    size = len(found['mdat@61437824']) - 8
    disk.seek(end)
    disk.seek(-size*c, 1)
    mdatHEAD = found['mdat@61437824'][:8]
    o.write(mdatHEAD)
    o.write(disk.read(size))
    o.write(found['moov@65087363'])


