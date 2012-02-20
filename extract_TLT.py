""" Extract Top-Level-Tags"""
import struct
def get_Tag_seek2next(f):
    while 1:
        dat = f.read(8)
        if dat:
            size = struct.unpack(">I",dat[:4])[0]
            f.seek(size-8,1)
            yield dat[4:]
            #yield ''.join([A,B,C,D])
        else:
            break
if __name__=="__main__":
    import sys
    if len(sys.argv) == 2:
        print list(get_Tag_seek2next(open(sys.argv[1],'rb')))
    else:
        print "Usage: python extract_TLT.py filename.mov"
