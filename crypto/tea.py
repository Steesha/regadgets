from typing import List, Tuple
from ctypes import c_uint32

def tea_encrypt(
    src: Tuple[int, int], key: List[int], delta: int = 0x9E3779B9, rounds: int = 32
):
    l, r = c_uint32(src[0]), c_uint32(src[1])
    sum = c_uint32(0)
    k = [c_uint32(i) for i in key]
    k = [c_uint32(key[0]), c_uint32(key[1]), c_uint32(key[2]), c_uint32(key[3])]
    for _ in range(rounds):
        sum.value += delta
        l.value += (
            ((r.value << 4) + k[0].value)
            ^ (r.value + sum.value)
            ^ ((r.value >> 5) + k[1].value)
        )
        r.value += (
            ((l.value << 4) + k[2].value)
            ^ (l.value + sum.value)
            ^ ((l.value >> 5) + k[3].value)
        )
    return (l.value, r.value)

def tea_decrypt(
    src: Tuple[int, int], key: List[int], delta: int = 0x9E3779B9, rounds: int = 32
):
    l, r = c_uint32(src[0]), c_uint32(src[1])
    sum = c_uint32(delta * rounds)
    k = [c_uint32(i) for i in key]
    for _ in range(rounds):
        r.value -= (
            ((l.value << 4) + k[2].value)
            ^ (l.value + sum.value)
            ^ ((l.value >> 5) + k[3].value)
        )
        l.value -= (
            ((r.value << 4) + k[0].value)
            ^ (r.value + sum.value)
            ^ ((r.value >> 5) + k[1].value)
        )
        sum.value -= delta
    return (l.value, r.value)