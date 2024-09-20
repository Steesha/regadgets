from typing import List
from struct import pack
from ctypes import c_uint32


def xxtea_std_shift(z, y, sum, k, p, e):
    return (((z.value >> 5) ^ (y.value << 2)) + ((y.value >> 3) ^ (z.value << 4))) ^ (
        (sum.value ^ y.value) + (k[(p & 3) ^ e.value].value ^ z.value)
    )


def xxtea_ciscn2024_shift(z, y, sum, k, p, e):
    return (
        (((z.value >> 5) ^ (y.value << 2)) + ((y.value >> 3) ^ (z.value << 4)))
        ^ ((sum.value ^ y.value))
    ) + (k[(p & 3) ^ e.value].value ^ z.value)


def xxtea_encrypt(
    src: List[int],
    key: List[int],
    delta: int = 0x9E3779B9,
    additional_rounds: int = 0,
    shift_func=xxtea_std_shift,
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
            src[p].value += shift_func(z, src[p + 1], sum, key, p, e)
            z = src[p]
        p += 1
        src[n - 1].value += shift_func(z, src[0], sum, key, p, e)
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
            src[p].value -= shift_func(src[p - 1], y, sum, key, p, e)
            y = src[p]
        p -= 1
        src[0].value -= shift_func(src[n - 1], y, sum, key, p, e)
        y = src[0]
        sum.value -= delta.value
    return [i.value for i in src]
