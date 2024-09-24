#! /usr/bin/env python
# vim: fileencoding=utf-8 

# From https://github.com/ysangkok/python-binary-in-utf8/blob/master/base128.py
# using bitarray.
#
# testing:
# py.test -s --doctest-modules base128.py

r"""
If called from command line, this encodes a binary file into base128.
If imported from python it provides a base128 class to do the same.
"""

import sys
import itertools
from bitarray import bitarray


class base128:
    r"""An instance of base128 can be used to convert to and from base128 encoding.

    Encoding: The python package bitarray is used to insert a 0 bit every 8
    bits of the data.  Bitarray cares to shift the bits to make room for the
    new bit.  This is done in chunks.  
    The length in bits mod 8 can become greater than zero for chunks of size
    not equal to a multiple of 7. So ``chunksize`` must be a multiple of 7.
    Even if ``chunksize`` is a multiple of 7 the last chunk 
    likely has to be padded to reach a multiple of 8 after encoding.
    The amount of padding can be expressed as a function of the original data
    length mod ``chunksize`` (``modchunk``). ``modchunk`` is added as an
    additional byte at the end of the encoding.  To make this byte also
    base128, we require ``chunksize``<=128.

    If ``chars`` is provided, the resulting 7-bit numbers are 
    used as indices to map to entries of ``chars``. 
    With bytes ``chars`` the resulting chunks will be integer lists 
    and possibly still need to be typed to bytes for further processing::

        with open('tstenc.txt','wb') as f: f.write(b'\n'.join([bytes(x) for x in encoded]))

    >>> _1 = base128.defaultchars
    >>> b128 = base128(chars=_1, chunksize=15)
    Traceback (most recent call last):
    ...
    AssertionError: chunksize must be a multiple of 7
    assert (15 % 7) == 0

    >>> b128 = base128(chars=_1, chunksize=133)
    Traceback (most recent call last):
    ...
    AssertionError: chunksize must be < 128
    assert 133 < 128

    >>> b128 = base128(chars="ab")
    Traceback (most recent call last):
    ...
    AssertionError: chars must have at least 128 entries
    assert (not 'ab' or 2 >= 128)
     +  where 2 = len('ab')

    >>> data = b"\x00\xff"
    >>> b128 = base128(chars=_1)
    >>> encoded = list(b128.encode(data))
    >>> decoded = b''.join(b128.decode(encoded))
    >>> decoded == data
    True

    >>> b128 = base128()
    >>> encoded = list(b128.encode(data))
    >>> decoded = b''.join(b128.decode(encoded))
    >>> decoded == data
    True

    A time hash:
    >>> from math import log
    >>> import time, calendar
    >>> epoch = calendar.timegm(time.strptime("17","%y"))
    >>> tm = time.time()
    >>> i = int(tm-epoch)#base on epoch 01012017
    >>> sizebytes = int(1+log(i)/log(256))
    >>> sizebytes
    4
    >>> data = i.to_bytes(sizebytes,byteorder='big')
    >>> b128 = base128(chars=_1)
    >>> encoded = list(b128.encode(data))
    >>> sizeencoded = len(encoded[0])
    >>> sizeencoded
    5
    >>> decoded = b''.join(b128.decode(encoded))
    >>> tm1 = epoch + int.from_bytes(decoded,byteorder='big')
    >>> sencoded = [bytes(x).decode('iso-8859-1') for x in encoded]
    >>> int(tm1-tm)==0
    True

    >>> import os
    >>> data = os.urandom(512)
    >>> b128 = base128(chars=_1, chunksize=14)
    >>> encoded = list(b128.encode(data))
    >>> sencoded = [bytes(x).decode('iso-8859-5') for x in encoded]
    >>> sencoded8859 = [x.encode('iso-8859-5')for x in sencoded]
    >>> decoded = b''.join(b128.decode(sencoded8859))
    >>> decoded == data
    True

    >>> b128 = base128()
    >>> encoded = list(b128.encode(data))
    >>> decoded = b''.join((b128.decode(encoded)))
    >>> decoded == data
    True

    >>> res1,res2 = [],[]
    >>> for i in range(126):
    ...     #i=3
    ...     data = os.urandom(513+i)
    ...     b128 = base128(chars=_1, chunksize=126)
    ...     encoded = list(b128.encode(data))
    ...     sencoded = [bytes(x).decode('iso-8859-1') for x in encoded]
    ...     decoded = b''.join(b128.decode(encoded))
    ...     res1.append(decoded == data)
    ...     b128 = base128()
    ...     encoded = b128.encode(data)
    ...     decoded = b''.join((b128.decode(encoded)))
    ...     res2.append(decoded == data)
    >>> all(res1) and all(res2)
    True

    """

    #all of these have same iso-8859 encoding
    utf8859 = {1:r'''0123456789ABCDEF
                     GHIJKLMNOPQRSTUV
                     WXYZabcdefghijkl
                     mnopqrstuvwxyzµ¶
                     ·¼½¾ÁÂÃÄÅÆÇÈÉÊËÌ
                     ÍÎÏÑÒÓÔÕÖ×ØÙÚÛÜÝ
                     Þßáâãäåæçèéêëìíî
                     ïñòóôõö÷øùúûüýþÿ''',
               5:r'''0123456789ABCDEF
                     GHIJKLMNOPQRSTUV
                     WXYZabcdefghijkl
                     mnopqrstuvwxyzЕЖ
                     ЗИЙКЛМНОПСТУФХЦЧ
                     ШЩЪЫЬЭЮЯбдежзийк
                     лмнопстуфхцчшщъы
                     ьэюяёђѓєѕіїјљњћќ''',
               7:r'''0123456789ABCDEF
                     GHIJKLMNOPQRSTUV
                     WXYZabcdefghijkl
                     mnopqrstuvwxyz΅Ά
                     ·ΈΉΊ»Ό½ΎΏΑΒΓΔΕΖΗ
                     ΘΙΚΛΜΝΞΟΡΤΥΦΧΨΩΪ
                     Ϋάέήίαβγδεζηθικλ
                     μνξορςστυφχψωϊϋό'''}

    defaultchars = rb''.join([x.strip().encode('iso-8859-1') for x in utf8859[1]])

    def __init__ (self, chars=None, chunksize = 7):
        """Initializes the base128 conversion instance

        chars -- is used as base128 code, if provided. It must be of length 128. 
                 Alternatively it can be True to use the default chars.
                 If omitted or False, chunks of integer lists are returned for encoding.

        chunksize -- determines the chunk size the input input data is split to.
        """
        assert chunksize % 7 == 0, "chunksize must be a multiple of 7"
        assert chunksize < 128, "chunksize must be < 128"
        if isinstance(chars,bool) and chars:
            chars = base128.defaultchars
        assert not chars or len(chars) >= 128, "chars must have at least 128 entries"
        self.chars = chars
        self.chunksize = chunksize

    @staticmethod
    def _chunks(iterable, size):
        """ http://stackoverflow.com/a/434314/309483 """
        it = iter(iterable)
        chunk = tuple(itertools.islice(it, size))
        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(it, size))

    def _encode_chunk(self, mbytes):
        mbinarr = bitarray()
        mbinarr.frombytes(bytes(mbytes))
        for pos in itertools.count(0,8):
            if pos >= len(mbinarr): break
            mbinarr.insert(pos,0)
        padlen = (8-(len(mbinarr)%8))%8
        inspos = len(mbinarr)-(len(mbinarr)%8)
        for i in range(padlen): 
            mbinarr.insert(inspos,0)
        mstring = mbinarr.tobytes()
        return mstring

    @staticmethod
    def _poscount(modchunk):
        "returns position and count of 0bit badding or None"
        mod7 = modchunk%7
        count = (7-mod7)%7
        if count:
            pos = 0
            nbits = modchunk*8
            while nbits:
                pos = pos + nbits
                nbits = ((nbits%8)+nbits)//8
            pos = pos-pos%8
            return pos, count
        return None, None

    def _decode_chunk(self, mstring, modchunk=None):
        mbinarr = bitarray()
        mbinarr.frombytes(mstring)
        if modchunk:
            pos,count = base128._poscount(modchunk)
            if pos:
                for i in range(count):
                    mbinarr.pop(pos)
        orglength = len(mbinarr)
        for i in itertools.count(0,8):
            pos = i - i//8
            if i > orglength-1: break
            mbinarr.pop(pos)
        return mbinarr.tobytes()

    #@staticmethod
    #def encoded_size(lendata):
    #    "returns the length of the encoded string given ``lendata`` of data"
    #    lenencoded = 0 
    #    nbits = lendata*8
    #    while nbits:
    #        lenencoded = lenencoded + nbits
    #        nbits = (nbits+(nbits%8))//8
    #    if lenencoded%8:
    #        nbits = 1
    #    lenencoded = lenencoded//8+nbits
    #    lenencoded = lenencoded + 1 #the modchunk byte 
    #    return lenencoded

    def encode(self,data):
        """Encodes into chunks of base128 bytes of size equal to a multiple of
        8, apart from the last chunk, which is of size 1 and contains the
        additional ``modchunk`` byte (encoded with chars if given).

        data -- is an iterable to bytes or convertibles to bytes
        """
        modchunk = len(data)%self.chunksize
        l1 = base128._chunks(data, self.chunksize)
        l2 = map(lambda mbytes: self._encode_chunk(mbytes), l1)
        for j in l2:
            st = j
            if self.chars:
                st = [self.chars[i] for i in j]
            yield st
        yield [self.chars and self.chars[modchunk] or modchunk]

    def decode(self, encoded):
        """Decode base128 chunks to the original data

        encoded -- must consist of chunks of size equal to a multiple of 8
                   apart from the last one of size 1 for the ``modchunk`` byte
        """
        mstring = None
        modchunk = None
        #mstring=encoded[-2]
        #item=encoded[-1]
        for item in encoded:
            if mstring:
                if len(item)==1:
                    modchunk = item[0]
                if self.chars:
                    if modchunk:
                        modchunk = self.chars.index(modchunk)
                    mstring = bytes([self.chars.index(i) for i in mstring])
                yield self._decode_chunk(mstring, modchunk)
            mstring = item


def main(args=None):
    import argparse

    def chksize(value):
        ivalue = int(value)
        if ivalue%7 != 0 or ivalue <= 0 or ivalue >= 128:
             raise argparse.ArgumentTypeError("chunksize must be a multiple of 7 smaller than 128")
        return ivalue

    def chkenc(value):
        if value == 'latin1':
            ivalue = 1
        elif value == 'cyrillic':
            ivalue = 5
        elif value == 'greek':
            ivalue = 7
        else:
            ivalue = int(value)
        if ivalue not in [1,5,7]:
             raise argparse.ArgumentTypeError("fenc must be 1, 5, 7, latin1, cyrillic or greek")
        return ivalue

    if args is None:
        parser = argparse.ArgumentParser(description = __doc__,
                formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        
        parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'))
        parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'))
        parser.add_argument('-e', '--encode', action='store_true', 
            help='Encode the input file')
        parser.add_argument('-d', '--decode', action='store_true', 
            help='Decode the input file')
        parser.add_argument('-f', '--fenc', action='store', default='1', type=chkenc, 
            help='In the encoded file add a file encoding line like "# vim: fileencoding=iso-8859-x"')
        parser.add_argument('-s', '--chunksize', action='store', default='70', type=chksize,
            help='Before encoding input data is split into chunk (multiple of 7 < 128)')

        args = parser.parse_args()

    enc = args.encode or args.decode

    assert enc and (not args.encode or not args.decode),"either provide encoding or decoding option (-e or -d)"

    b128 = base128(chars = base128.defaultchars, chunksize = args.chunksize)
    data = args.infile.read(-1)

    if args.encode:
        encoded = list(b128.encode(data))
        encoded[-2].extend(encoded[-1])
        del encoded[-1]
        sencoded = b'\n'.join([bytes(x) for x in encoded])
        header = b"# vim: fileencoding=iso-8859-"+str(args.fenc).encode()
        w = header+b'\n\n'+sencoded
        args.outfile.write(w)
    elif args.decode:
        encoded = data
        encoded = encoded.splitlines()
        if len(encoded)>1 and b'fileencoding=' in encoded[0]:
            enc = encoded[0].split(b'fileencoding=')[1].decode()
            del encoded[0]
            while len(encoded) > 0 and len(encoded[0])==0:
                del encoded[0]
        if len(encoded) > 0:
            if len(encoded[-1]) != 1: #no separate modchunk
                encoded.append([encoded[-1][-1]]) #make one
                encoded[-2] = encoded[-2][:-1]
        decoded = b''.join(b128.decode(encoded))
        args.outfile.write(decoded)


if __name__ == '__main__':
    main()
