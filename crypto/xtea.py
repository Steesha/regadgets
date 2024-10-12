from typing import List, Tuple, Union
from ctypes import c_uint32
from ..bits.bits import byte2dword, dword2byte, pack_dword

def xtea_encrypt(
    src: Union[Tuple[int, int], bytes, List[int]], key: List[int], delta: int = 0x9E3779B9, rounds: int = 32
) -> Union[Tuple[int, int], bytes, List[int]]:
    if type(src) == bytes:
        result = b''
        for i in pack_dword(byte2dword(src)):
            result += dword2byte(xtea_decrypt(i, key, delta, rounds))
        return result
    elif type(src) == list:
        result = b''
        for i in pack_dword(src):
            result += dword2byte(xtea_decrypt(i, key, delta, rounds))
        return result
    l, r = c_uint32(src[0]), c_uint32(src[1])
    sum = c_uint32(0)
    k = [c_uint32(key[0]), c_uint32(key[1]), c_uint32(key[2]), c_uint32(key[3])]
    for _ in range(rounds):
        l.value += (((r.value << 4) ^ (r.value >> 5)) + r.value) ^ (
            sum.value + k[sum.value & 3].value
        )
        sum.value += delta
        r.value += (((l.value << 4) ^ (l.value >> 5)) + l.value) ^ (
            sum.value + k[(sum.value >> 11) & 3].value
        )
    return (l.value, r.value)

def xtea_decrypt(
    src: Union[Tuple[int, int], bytes, List[int]], key: List[int], delta: int = 0x9E3779B9, rounds: int = 32
) -> Union[Tuple[int, int], bytes, List[int]]:
    if type(src) == bytes:
        result = b''
        for i in pack_dword(byte2dword(src)):
            result += dword2byte(xtea_decrypt(i, key, delta, rounds))
        return result
    elif type(src) == list:
        result = b''
        for i in pack_dword(src):
            result += dword2byte(xtea_decrypt(i, key, delta, rounds))
        return result
    l, r = c_uint32(src[0]), c_uint32(src[1])
    sum = c_uint32(delta * rounds)
    k = [c_uint32(key[0]), c_uint32(key[1]), c_uint32(key[2]), c_uint32(key[3])]
    for _ in range(rounds):
        r.value -= (((l.value << 4) ^ (l.value >> 5)) + l.value) ^ (
            sum.value + k[(sum.value >> 11) & 3].value
        )
        sum.value -= delta
        l.value -= (((r.value << 4) ^ (r.value >> 5)) + r.value) ^ (
            sum.value + k[sum.value & 3].value
        )
    return (l.value, r.value)