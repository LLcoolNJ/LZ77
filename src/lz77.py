import sys
from bitarray import bitarray

class lz77:
    """It is python implementation of well known compression algorithm
        known as LZ77.
    """
    searchBufferSize = 250
    lookABufferSize = 250
    def __init__(self):
        pass
    def sch(self,lookABuffer, searchBuffer):
        """It search for the pattern from look aside buffer in search buffer 
            with maximun size match. And it returns the offset starting of 
            pattern in look aside buffer and pattern's length.
        """
        offset = 0
        length = 0
        for i in xrange(1, self.searchBufferSize+1):
            l = 0
            o = 0
            if searchBuffer[self.searchBufferSize - i ] is None:
                if l >= length:
                    length = l
                    offset = i
                break
            for j in xrange(i):
                if j  >= len(lookABuffer)-1:
                    if l >= length:
                        length = l
                        offset = i 
                    break
                if searchBuffer[self.searchBufferSize - i + j] == lookABuffer[j]:
                    l += 1
                else:
                    if l >= length:
                        length = l
                        offset = i
                    break
                if l == i:
                    if l >= length:
                        length = l
                        offset = i
                    break
        return length,offset
    def compress(self,file,DEBUG=False):
        """compress(inputFileLocations, DEBUG)
            Give the input file locations as first argument and for debugging provide second argument 
            as True
            
            Data representation:
            if pattern found then 1 flag bit three 8 bit chars - total: 25 bits
            else 1 flag bit single 8 bit char - total: 9 bits
                
            It will write the compressed data in 
        """
        try:
            with open(file,'rb') as f:
                s = list(f.read())
        except IOError:
            print 'Unable to open file'
            exit(1)
        # print s
        outFile = file.split('.')
        ext = outFile[-1]
        outFile = ''.join(outFile[:-1] + ['.lz77'])
        l = len(ext)
        out = bitarray(endian='big')
        out.frombytes(chr(l))
        for i in ext:
            out.frombytes(i)
        searchBuffer = [None]*self.searchBufferSize
        lookABuffer = s[:self.lookABufferSize]
        s = s[self.lookABufferSize:]
        while len(lookABuffer) != 0:
            length,offset = self.sch(lookABuffer, searchBuffer)
            try:
                symbol = lookABuffer[length]
            except IndexError:
                symbol = '$'
            if length > 0:
                if symbol == '$' and len(s) > 0:
                    symbol = s[0]
                    searchBuffer.extend(lookABuffer + [symbol])
                    searchBuffer = searchBuffer[length + 1:]
                    lookABuffer.extend(s[:length+1])
                    s = s[length+1:]
                    lookABuffer = lookABuffer[length+1:]
                else:
                    searchBuffer.extend(lookABuffer[:length+1])
                    searchBuffer = searchBuffer[length + 1:]
                    lookABuffer.extend(s[:length+1])
                    s = s[length+1:]
                    lookABuffer = lookABuffer[length+1:]
                    if DEBUG:
                        print offset,length,symbol
            else:
                if DEBUG:
                    print 0,symbol
                searchBuffer.pop(0)
                e = lookABuffer.pop(0)
                searchBuffer.append(e)
                try:
                    e = s.pop(0)
                    lookABuffer.append(e)
                except:
                    pass
            if offset != 0:
                out.append(True)
                out.frombytes(chr(offset))
                out.frombytes(chr(length))
                out.frombytes(symbol)
            else:
                out.append(False)
                out.frombytes(symbol)
        out.fill()
        try:
            with open(outFile,'wb') as f:
                f.write(out.tobytes())
        except IOError:
            print 'Unable to write compressed file'
            exit(1)
    def decompress(self,file,DEBUG = False):
        """decompress(inputFileLocations, DEBUG)
            Give the input file locations as first argument and for debugging provide second argument 
            as True
            
            It will write in dfile.txt the decompressed data.
        """
        data = bitarray(endian='big')
        res = []
        try:
            with open(file,'rb') as f:
                data.fromfile(f)
        except IOError:
            print 'Unable to read compressed file'
            exit(1)
            
        ext = '.'
        l = ord(data[:8].tobytes())
        del(data[:8])
        while l >0:
            ext += data[:8].tobytes()
            del(data[:8])
            l -= 1
        while len(data) >= 9:
            flag = data.pop(0)
            if not flag:
                symbol = data[0:8].tobytes()
                offset = 0
                length = 0
                del(data[0:8])
                if DEBUG:
                    print 0,0,symbol
            else:
                offset = ord(data[0:8].tobytes())
                length = ord(data[8:16].tobytes())
                symbol = data[16:24].tobytes()
                if DEBUG:
                    print offset,length,symbol
                del(data[:24])
            x = []
            if -offset + length >= 0:
                x = res[-offset:] + res[:-offset + length] + [symbol]
            else:
                x = res[-offset:-offset + length] + [symbol]
            res.extend(x)
            # print res
        if res[-1] == '$':
            res.pop()
        v = ''.join(res)
        # print v
        outFile = ''.join(file.split('.')[:-1] + [ext])
        try:
            with open(outFile,'wb') as f:
                f.write(v)
        except IOError:
            print 'Unable to write decompressed file'
            exit()
if __name__ == '__main__':
    arg = sys.argv[1:]
    if arg[0] == '-h' or arg[0] == '--h' or arg[0] == '-help':
        print "usage lz77.py [-c | -d ] filename"
        print "option:"
        print "-c\t\t\t:Compress data."
        print "-d\t\t\t:Decompress data."
        exit(0)
    elif arg[0] == '-c':
        l = lz77()
        try:
            print 'Compressing...'
            l.compress(arg[1])
        except:
            print 'Compression Unseccessfull.' 
            exit(1)
        print 'Compression Seccessfull.' 
    elif arg[0] == '-d':
        l = lz77()
        try:
            print 'Decompressing...'
            l.decompress(arg[1])
        except:
            print 'Decompression Unseccessfull'
            exit(1)
        print 'Decompression Seccessfull'
    else:
        print "Invalid input"
        print "usage script.py [-c | -d ] filename"
        print "option:"
        print "-c\t\t\t:Compress data."
        print "-d\t\t\t:Decompress data."
        exit(0)