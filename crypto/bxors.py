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

def bxor(data1: bytes | list, data2: bytes | list) -> bytes:
    if len(data1) != len(data2):
        return b''
    return bytes([i ^ j for i, j in zip(data1, data2)])