# -*- coding: utf-8 -*-

__version__ = (1, 1, 0)


class Base92(object):
    # Base92有效字符集，共91个，其中~为占位符，未写入有效字符集(The valid character set of base92, ~ is a placeholder, not in character set.)
    CHARACTER_SET = r"!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}"

    @classmethod
    def base92_chr(cls, val):
        """
        将小于91的整数映射成对应的字符
        Map an integer value <91 to a char
        """
        if val < 0 or val >= 91:
            raise ValueError('val must be in [0, 91)')
        if val == 0:
            return '!'
        elif val <= 61:
            return chr(ord('#') + val - 1)
        else:
            return chr(ord('a') + val - 62)

    @classmethod
    def base92_ord(cls, val):
        '''
        将字符映射成对应的整数
        Map a char to an integer
        '''
        num = ord(val)
        if val == '!':
            return 0
        elif ord('#') <= num and num <= ord('_'):
            return num - ord('#') + 1
        elif ord('a') <= num and num <= ord('}'):
            return num - ord('a') + 62
        else:
            raise ValueError('val is not a base92 character')

    @classmethod
    def get_character_set(cls):
        return cls.CHARACTER_SET

    @classmethod
    def b92encode(cls, byt: bytes) -> str:
        if not isinstance(byt, bytes):
            raise TypeError(f"a bytes-like object is required, not '{type(byt)}'")
        if not byt:
            return '~'
        # 确保bytstr存在(make sure we have a bytstr)
        if not isinstance(byt, str):
            # 假定整数序列(we'll assume it's a sequence of ints)
            byt = ''.join([chr(b) for b in byt])
        # 实现(Implementation measure)
        bitstr = ''
        while len(bitstr) < 13 and byt:
            bitstr += '{:08b}'.format(ord(byt[0]))
            byt = byt[1:]
        resstr = ''
        while len(bitstr) > 13 or byt:
            i = int(bitstr[:13], 2)
            resstr += cls.base92_chr(i // 91)
            resstr += cls.base92_chr(i % 91)
            bitstr = bitstr[13:]
            while len(bitstr) < 13 and byt:
                bitstr += '{:08b}'.format(ord(byt[0]))
                byt = byt[1:]

        if bitstr:
            if len(bitstr) < 7:
                bitstr += '0' * (6 - len(bitstr))
                resstr += cls.base92_chr(int(bitstr, 2))
            else:
                bitstr += '0' * (13 - len(bitstr))
                i = int(bitstr, 2)
                resstr += cls.base92_chr(i // 91)
                resstr += cls.base92_chr(i % 91)
        return resstr

    @classmethod
    def b92decode(cls, bstr: str) -> bytes:
        if not isinstance(bstr, str):
            raise TypeError(f"a str object is required, not '{type(bstr)}'")
        bitstr = ''
        resstr = ''
        if bstr == '~':
            return ''.encode(encoding='latin-1')

        for i in range(len(bstr) // 2):
            x = cls.base92_ord(bstr[2 * i]) * 91 + cls.base92_ord(bstr[2 * i + 1])
            bitstr += '{:013b}'.format(x)
            while 8 <= len(bitstr):
                resstr += chr(int(bitstr[0:8], 2))
                bitstr = bitstr[8:]
        # 检查额外的字符(Check for extra characters.)
        if len(bstr) % 2 == 1:
            x = cls.base92_ord(bstr[-1])
            bitstr += '{:06b}'.format(x)
            while 8 <= len(bitstr):
                resstr += chr(int(bitstr[0:8], 2))
                bitstr = bitstr[8:]
        return resstr.encode(encoding='latin-1')
