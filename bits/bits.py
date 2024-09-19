from typing import List
from struct import pack, unpack

def ror8(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xFF
def rol8(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xFF

def rol16(x, n):
    return ((x << n) | (x >> (16 - n))) & 0xFFFF
def ror16(x, n):
    return ((x >> n) | (x << (16 - n))) & 0xFFFF

def rol32(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
def ror32(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def rol64(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF
def ror64(x, n):
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF


def byte2dword(x: List[int] | bytes):
    if len(x) % 4 != 0:
        if type(x) == bytes:
            x += b'\x00' * (4 - (len(x) % 4))
        else:
            x += [0] * (4 - (len(x) % 4))
    return [v[0] for v in (unpack('<I', bytes(x[i:i+4])) for i in range(0, len(x), 4))]

def dword2bytes(x: List[int] | int):
    result = []
    if type(x) == int:
        for j in range(4):
            result.append((x >> j*8) & 0xff)
        return bytes(result)
    for i in range(len(x)):
        for j in range(4):
            result.append((x[i] >> j*8) & 0xff)
    return bytes(result)