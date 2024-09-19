from typing import List
from struct import pack
def xxtea_std_shift(z, y, sum, k, p, e):
    return (
            (  ((z >> 5) ^ (y << 2)) +  ((y >> 3) ^ (z << 4))  )
            ^
            (       (sum ^ y)        +   (k[(p & 3) ^ e] ^ z)  )
        )

def xxtea_ciscn2024_shift(z, y, sum, k, p, e):
    return ( 
            (  ((z >> 5) ^ (y << 2)) +  ((y >> 3) ^ (z << 4))  )
            ^ 
            (       (sum ^ y)                                  )
        )                            +   (k[(p & 3) ^ e] ^ z)
            
def xxtea_encrypt(src: list, key: List[int], delta: int = 0x9e3779b9, 
                  additional_rounds: int = 0, shift_func = xxtea_std_shift):
    delta &= 0xffffffff
    n = len(src)
    rounds = 6 + 52 // n + additional_rounds
    sum = 0
    z = src[n - 1]
    for _ in range(rounds):
        sum = (sum + delta) & 0xFFFFFFFF
        e = (sum >> 2) & 3
        for i in range(n - 1):
            y = src[i + 1]
            src[i] = (src[i] + shift_func(z, y, sum, key, i, e)) & 0xFFFFFFFF
            z = src[i]
        i += 1
        src[n - 1] = (src[n - 1] + shift_func(z, src[0], sum, key, i, e)) & 0xFFFFFFFF
        z = src[n - 1]
    return src

# To reverse xxtea, you need to know:
# function shift, delta, addition_rounds.
def xxtea_decrypt(src: list, key: List[int], delta: int = 0x9E3779B9, 
                  additional_rounds: int = 0, shift_func = xxtea_std_shift):
    delta &= 0xffffffff
    n = len(src)
    rounds = 6 + 52 // n + additional_rounds
    sum = (rounds * delta) & 0xFFFFFFFF
    y = src[0]
    for _ in range(rounds):
        e = (sum >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = src[p - 1]
            src[p] = (src[p] - shift_func(z, y, sum, key, p, e)) & 0xFFFFFFFF
            y = src[p]
        p -= 1
        z = src[n - 1]
        src[0] = (src[0] - shift_func(z, y, sum, key, p, e)) & 0xFFFFFFFF
        y = src[0]
        sum = (sum - delta) & 0xFFFFFFFF
    return src