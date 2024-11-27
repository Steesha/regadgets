from typing import Union, List
# NOTE:
# bxorr_dec(bxorr_enc(x)) == bxorr_enc(bxorr_dec(x)) == x
# From: x_0 ^ x_1, x_1 ^ x_2, x_2 ^ x_3, ..... , x_(n-1) ^ x_n, x_n
def bxorr_dec(encrypted: bytes) -> bytes:
    result = []
    _last = encrypted[-1]
    result.append(_last)
    for i in encrypted[::-1][1:]:
        i ^= _last
        _last = i
        result.append(i)
    return bytes(result[::-1])

# From: x_0 , x_1 ^ x_0, x_2 ^ x_1, ..... , x_(n-1) ^ x_n
def bxorl_dec(encrypted: bytes) -> bytes:
    encrypted = encrypted[::-1]
    return bxorr_dec(encrypted)[::-1]

# NOTE:
# bxorr_dec(bxorr_enc(x)) == bxorr_enc(bxorr_dec(x)) == x
# To: x_0 ^ x_1, x_1 ^ x_2, x_2 ^ x_3, ..... , x_(n-1) ^ x_n, x_n
def bxorr_enc(raw: bytes) -> bytes:
    _last = 0
    result = []
    for i in range(len(raw) - 1):
        result.append(raw[i] ^ raw[i + 1])
    result.append(raw[-1])
    return bytes(result)

# To: x_0 , x_1 ^ x_0, x_2 ^ x_1, ..... , x_(n-1) ^ x_n
def bxorl_enc(encrypted: bytes) -> bytes:
    return bxorr_enc(encrypted[::-1])[::-1]

def bxor(data1: bytes, data2: bytes) -> bytes:
    if len(data1) != len(data2):
        return b''
    return bytes([i ^ j for i, j in zip(data1, data2)])

def bxor_cycle(data1: Union[bytes, List[int]], data_cycle: Union[bytes, int, List[int]]) -> Union[bytes, List[int]]:
    if type(data_cycle) == int:
        data_cycle = [data_cycle]
    result = []
    for i in range(len(data1)):
        result.append(data1[i] ^ data_cycle[i % len(data_cycle)])
    if type(data1) == list:
        return result
    else:
        return bytes(result)