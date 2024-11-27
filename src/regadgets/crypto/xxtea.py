from typing import List, Union
from ctypes import c_uint32
from ..bits import byte2dword, dword2byte

def xxtea_std_shift(z, y, sum, k, p, debug = False):
    if debug:
        print("-----------------XXTEA_STD_SHIFT-----------------")
    e = (sum.value >> 2) & 3
    PE = (p & 3) ^ e
    Ly = y.value << 2
    Ry = y.value >> 3
    Lz = z.value << 4
    Rz = z.value >> 5 

    LzRy = Rz ^ Ly
    LyRz = Ry ^ Lz
    SY = sum.value ^ y.value
    K = k[PE].value
    KZ = K ^ z.value
    result = (LzRy + LyRz) ^ (KZ + SY)
    if debug:
        print("sum = ", hex(sum.value & 0xffffffff))
        print("e   = ", hex(e & 0xffffffff))
        print("PE  = ", hex(PE & 0xffffffff))
        print("SY  = ", hex(SY & 0xffffffff))
        print("z   = ", hex(z.value & 0xffffffff))
        print("y   = ", hex(y.value & 0xffffffff))
        print("Ly  = ", hex(Ly & 0xffffffff))
        print("Ry  = ", hex(Ry & 0xffffffff))
        print("Lz  = ", hex(Lz & 0xffffffff))
        print("Rz  = ", hex(Rz & 0xffffffff))
        print("LzRy= ", hex(LzRy & 0xffffffff))
        print("LyRz= ", hex(LyRz & 0xffffffff))
        print("K   = ", hex(K & 0xffffffff))
        print("KZ  = ", hex(KZ & 0xffffffff))
        print("ret = ", hex(result & 0xffffffff))
        print("-----------------XXTEA_STD_SHIFT-----------------")
    return result

def xxtea_ciscn2024_shift(z, y, sum, k, p, debug = False):
    e = (sum.value >> 2) & 3
    PE = (p & 3) ^ e
    Ly = y.value << 2
    Ry = y.value >> 3
    Lz = z.value << 4
    Rz = z.value >> 5 

    LzRy = Rz ^ Ly
    LyRz = Ry ^ Lz
    SY = sum.value ^ y.value
    K = k[PE].value
    KZ = K ^ z.value
    result = ((LzRy + LyRz) ^ SY) + KZ
    return result

def xxtea_encrypt(
    src: Union[List[int], bytes],
    key: Union[List[int], bytes],
    delta: int = 0x9E3779B9,
    round_base: int = 6,
    round_addi: int = 52,
    shift_func=xxtea_std_shift,
    debug=False,
) -> Union[List[int], bytes]:
    in_bytes = False
    if type(src) == bytes:
        src = byte2dword(src)
        in_bytes = True
    if type(key) == bytes:
        key = byte2dword(key)
    if in_bytes:
        return dword2byte(xxtea_encrypt(src, key, delta, round_base, round_addi, shift_func, debug))
    src = [c_uint32(i) for i in src]
    key = [c_uint32(i) for i in key]
    sum, e = c_uint32(0), c_uint32(0)
    delta = c_uint32(delta)
    n = len(src)
    rounds = round_base + round_addi // n
    z = src[n - 1]
    for _ in range(rounds):
        sum.value += delta.value
        for p in range(n - 1):
            y = src[p + 1]
            shift_result = shift_func(z, y, sum, key, p, debug)
            src[p].value += shift_result
            z = src[p]
        p += 1
        y = src[0]
        shift_result = shift_func(z, y, sum, key, p, debug)
        src[n - 1].value += shift_result
        z = src[n - 1]
    return [i.value for i in src]


# To reverse xxtea, you need to know:
# function shift, delta, addition_rounds.
def xxtea_decrypt(
    src: Union[List[int], bytes],
    key: List[int],
    delta: int = 0x9E3779B9,
    round_base: int = 6,
    round_addi: int = 52,
    shift_func=xxtea_std_shift,
    debug=False,
) -> Union[List[int], bytes]:
    in_bytes = False
    if type(src) == bytes:
        src = byte2dword(src)
        in_bytes = True
    if type(key) == bytes:
        key = byte2dword(key)
    if in_bytes:
        return dword2byte(xxtea_decrypt(src, key, delta, round_base, round_addi, shift_func, debug))
    src = [c_uint32(i) for i in src]
    key = [c_uint32(i) for i in key]
    sum, e, y = c_uint32(0), c_uint32(0), c_uint32(0)
    delta = c_uint32(delta)
    n = len(src)
    rounds = round_base + round_addi // n
    sum.value = rounds * delta.value
    y = src[0]
    for _ in range(rounds):
        for p in range(n - 1, 0, -1):
            z = src[p - 1]
            shift_result = shift_func(z, y, sum, key, p, debug)
            src[p].value -= shift_result 
            y = src[p]
        p -= 1
        z = src[n - 1]
        shift_result = shift_func(z, y, sum, key, p, debug)
        src[0].value -= shift_result
        y = src[0]
        sum.value -= delta.value
    return [i.value for i in src]
