from typing import List, Tuple
def xtea_encrypt(src: Tuple[int, int], key: List[int], delta: int = 0x9e3779b9, rounds: int = 32):
    l, r = src
    l &= 0xffffffff
    r &= 0xffffffff
    sum = 0
    for _ in range(rounds):
        l += (((r << 4) ^ (r >> 5)) + r) ^ (sum + key[sum & 3])
        l &= 0xFFFFFFFF

        sum += delta
        sum &= 0xFFFFFFFF

        r += (((l << 4) ^ (l >> 5)) + l) ^ (sum + key[(sum >> 11) & 3])
        r &= 0xFFFFFFFF

    return (l, r)


def xtea_decrypt(src: Tuple[int, int], key: List[int], delta: int = 0x9e3779b9, rounds: int = 32):
    l, r = src
    l &= 0xffffffff
    r &= 0xffffffff
    sum = (rounds * delta) & 0xffffffff
    for _ in range(rounds):
        r -= (((l << 4) ^ (l >> 5)) + l) ^ (sum + key[(sum >> 11) & 3])
        r &= 0xFFFFFFFF

        sum -= delta
        sum &= 0xFFFFFFFF

        l -= (((r << 4) ^ (r >> 5)) + r) ^ (sum + key[sum & 3])
        l &= 0xFFFFFFFF


    return (l, r)