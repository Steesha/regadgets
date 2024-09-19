from typing import List, Tuple
def tea_encrypt(src: Tuple[int, int], key: List[int], delta: int = 0x9e3779b9, rounds: int = 32):
    l, r = src
    l &= 0xffffffff
    r &= 0xffffffff
    sum = 0
    k0, k1, k2, k3 = key[0], key[1], key[2], key[3]
    for _ in range(rounds):
        sum += delta
        sum &= 0xFFFFFFFF

        l += ((r << 4) + k0) ^ (r + sum) ^ ((r >> 5) + k1)
        l &= 0xFFFFFFFF

        r += ((l << 4) + k2) ^ (l + sum) ^ ((l >> 5) + k3)
        r &= 0xFFFFFFFF
    return (l, r)


def tea_decrypt(src: Tuple[int, int], key: List[int], delta: int = 0x9e3779b9, rounds: int = 32):
    l, r = src
    l &= 0xffffffff
    r &= 0xffffffff
    sum = (delta * rounds) & 0xffffffff
    k0, k1, k2, k3 = key[0], key[1], key[2], key[3]
    for _ in range(rounds):
        r -= ((l << 4) + k2) ^ (l + sum) ^ ((l >> 5) + k3)
        r &= 0xFFFFFFFF

        l -= ((r << 4) + k0) ^ (r + sum) ^ ((r >> 5) + k1)
        l &= 0xFFFFFFFF

        sum -= delta
        sum &= 0xFFFFFFFF

    return (l, r)