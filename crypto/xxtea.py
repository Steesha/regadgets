from typing import List
from struct import pack
from ctypes import c_uint32

def print_shift_debug(z, y, sum, k, p, e, result):
    print('----------------------XXTEA-DEBUG----------------------')
    print('z', z.value, hex(z.value))
    print('y', y.value, hex(y.value))
    print('sum', sum.value, hex(sum.value))
    print('p', p, hex(p))
    print('e', e.value, hex(e.value))
    print('z >> 5', (z.value >> 5) & 0xffffffff, hex((z.value >> 5) & 0xffffffff))
    print('y << 2', (y.value << 2) & 0xffffffff, hex((y.value << 2) & 0xffffffff))
    print('y >> 3', (y.value >> 3) & 0xffffffff, hex((y.value >> 3) & 0xffffffff))
    print('z << 4', (z.value << 4) & 0xffffffff, hex((z.value << 4) & 0xffffffff))
    print('sum ^ y', '   ', (sum.value ^ y.value) & 0xffffffff, hex((sum.value ^ y.value) & 0xffffffff))
    print('(p&3)^e', '   ', k[(p & 3) ^ e.value].value & 0xffffffff, hex(k[(p & 3) ^ e.value].value & 0xffffffff))
    print('k[(p&3)^e] ^ z', '                        ', k[(p & 3) ^ e.value].value ^ z.value, hex(k[(p & 3) ^ e.value].value ^ z.value))
    print('$1 = [(z>>5)^(y<<2)]+[(y>>3)^(z<<4)]', '  ',((((z.value >> 5) ^ (y.value << 2)) + ((y.value >> 3) ^ (z.value << 4)))) & 0xffffffff,
          hex((((z.value >> 5) ^ (y.value << 2)) + ((y.value >> 3) ^ (z.value << 4))) & 0xffffffff))
    print('$2 = (sum^y)+(k[(p&3)^e]^z)', '           ', ((sum.value ^ y.value) + (k[(p & 3) ^ e.value].value ^ z.value)) & 0xffffffff, 
          hex(((sum.value ^ y.value) + (k[(p & 3) ^ e.value].value ^ z.value)) & 0xffffffff))
    print('result = $1 ^ $2', '                      ', result & 0xffffffff, hex(result & 0xffffffff))
    print('----------------------XXTEA-DEBUG----------------------')


def xxtea_std_shift(z, y, sum, k, p, e):
    result = (((z.value >> 5) ^ (y.value << 2)) + ((y.value >> 3) ^ (z.value << 4))) ^ (
        (sum.value ^ y.value) + (k[(p & 3) ^ e.value].value ^ z.value)
    )
    return result


def xxtea_ciscn2024_shift(z, y, sum, k, p, e):
    result = (
        (((z.value >> 5) ^ (y.value << 2)) + ((y.value >> 3) ^ (z.value << 4)))
        ^ ((sum.value ^ y.value))
    ) + (k[(p & 3) ^ e.value].value ^ z.value)
    return result


def xxtea_encrypt(
    src: List[int],
    key: List[int],
    delta: int = 0x9E3779B9,
    additional_rounds: int = 0,
    shift_func=xxtea_std_shift,
    debug=False,
):
    src = [c_uint32(i) for i in src]
    key = [c_uint32(i) for i in key]
    sum, e = c_uint32(0), c_uint32(0)
    delta = c_uint32(delta)
    n = len(src)
    rounds = 6 + 52 // n + additional_rounds
    z = src[n - 1]
    for _ in range(rounds):
        sum.value += delta.value
        e.value = (sum.value >> 2) & 3
        for p in range(n - 1):
            y = src[p + 1]
            shift_result = shift_func(z, y, sum, key, p, e)
            src[p].value += shift_result
            ###
            if debug:
                print_shift_debug(z, y, sum, key, p, e, shift_result)
            ###
            z = src[p]
        p += 1
        y = src[0]
        shift_result = shift_func(z, y, sum, key, p, e)
        src[n - 1].value += shift_result
        ###
        if debug:
            print_shift_debug(z, y, sum, key, p, e, shift_result)
        ###
        z = src[n - 1]
    return [i.value for i in src]


# To reverse xxtea, you need to know:
# function shift, delta, addition_rounds.
def xxtea_decrypt(
    src: List[int],
    key: List[int],
    delta: int = 0x9E3779B9,
    additional_rounds: int = 0,
    shift_func=xxtea_std_shift,
    debug=False,
):
    src = [c_uint32(i) for i in src]
    key = [c_uint32(i) for i in key]
    sum, e, y = c_uint32(0), c_uint32(0), c_uint32(0)
    delta = c_uint32(delta)
    n = len(src)
    rounds = 6 + 52 // n + additional_rounds
    sum.value = rounds * delta.value
    y = src[0]
    for _ in range(rounds):
        e.value = (sum.value >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = src[p - 1]
            shift_result = shift_func(z, y, sum, key, p, e)
            src[p].value -= shift_result 
            ###
            if debug:
                print_shift_debug(z, y, sum, key, p, e, shift_result)
            ###
            y = src[p]
        p -= 1
        z = src[n - 1]
        shift_result = shift_func(z, y, sum, key, p, e)
        src[0].value -= shift_result
        ###
        if debug:
            print_shift_debug(z, y, sum, key, p, e, shift_result)
        ###
        y = src[0]
        sum.value -= delta.value
    return [i.value for i in src]
