#LZ77 Compressor#

---

###A simple python script to compress and decompress using lz77 compression algorithm.

##Implementation

---

It follows the standard implementation of lz77 compression algorithm . It search for the pattern from `look aside buffer` in `search buffer` with `maximun size match`. And it returns the offset starting of pattern in look aside buffer and pattern's length.


##Usage

---

usage lz77.py [-c | -d ] filename

option:

-c :Compress data.

-d :Decompress data.

##Includes

---

1. file.txt : Uncompressed file. size: 9,869 bytes

2. file.lz77 : Compressed file. size: 9,033 bytes
