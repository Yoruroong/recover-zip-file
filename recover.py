import sys

filename = input("손상된 파일 이름 : ") # ask file name

class FileHeader:
    SIGNATURE = b'PK\x03\x04' # header signiture
    def __init__(self, f):
        self.readHeader(f) # readfile
 
    def readHeader(self, f):
        sign = f.read(4)
        if sign != FileHeader.SIGNATURE:
            f.seek(-4, 1)
            raise Exception("Wrong Format")
        self.ver = int.from_bytes(f.read(2), 'little')
        self.bitflag = int.from_bytes(f.read(2), 'little')
        self.method = int.from_bytes(f.read(2), 'little')
        self.modTime = int.from_bytes(f.read(2), 'little')
        self.modDate = int.from_bytes(f.read(2), 'little')
        self.crc = int.from_bytes(f.read(4), 'little')
        self.compSize = int.from_bytes(f.read(4), 'little')
        self.rawSize = int.from_bytes(f.read(4), 'little')
        self.nameLen = int.from_bytes(f.read(2), 'little')
        self.extLen = int.from_bytes(f.read(2), 'little')
        self.name = f.read(self.nameLen)
        self.ext = f.read(self.extLen)
 
    def writeHeader(self, f):
        f.write(FileHeader.SIGNATURE)
        f.write(self.ver.to_bytes(2, 'little'))
        f.write(self.bitflag.to_bytes(2, 'little'))
        f.write(self.method.to_bytes(2, 'little'))
        f.write(self.modTime.to_bytes(2, 'little'))
        f.write(self.modDate.to_bytes(2, 'little'))
        f.write(self.crc.to_bytes(4, 'little'))
        f.write(self.compSize.to_bytes(4, 'little'))
        f.write(self.rawSize.to_bytes(4, 'little'))
        f.write(self.nameLen.to_bytes(2, 'little'))
        f.write(self.extLen.to_bytes(2, 'little'))
        f.write(self.name)
        f.write(self.ext)
 
 
w = open('restored.' + filename, 'wb')
with open(filename, 'rb') as f:
    notEnd = True
    while notEnd:
        try:
            hd = FileHeader(f)
            comps = f.read(hd.compSize)
            print(hd.name.decode('utf-8'))
            hd.writeHeader(w)
            w.write(comps)
            w.flush()
        except:
            for _ in range(1000):
                ch = f.read(16384)
                notEnd = len(ch) == 16384
                f.seek(-16384, 1)
                t = ch.find(b'PK\x03\x04')
                if t >= 0:
                    f.seek(t, 1)
                    break
                f.seek(16380, 1)
            else: continue
            print('Restore pos found!')
w.close()
