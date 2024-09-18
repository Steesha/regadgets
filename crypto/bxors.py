# NOTE:
# bxorr_dec(bxorr_enc(x)) == bxorr_enc(bxorr_dec(x)) == x
# From: x_0 ^ x_1, x_1 ^ x_2, x_2 ^ x_3, ..... , x_(n-1) ^ x_n, x_n ^ ends_xor
def bxorr_dec(encrypted: bytes, ends_xor: int = 0) -> bytes:
    ends_xor &= 0xff
    result = []
    _last = encrypted[-1] ^ ends_xor
    result.append(_last)
    for i in encrypted[::-1][1:]:
        i ^= _last
        _last = i
        result.append(i)
    return bytes(result[::-1])

# NOTE:
# bxorr_dec(bxorr_enc(x)) == bxorr_enc(bxorr_dec(x)) == x
# To: x_0 ^ x_1, x_1 ^ x_2, x_2 ^ x_3, ..... , x_(n-1) ^ x_n, x_n ^ ends_xor
def bxorr_enc(raw: bytes, ends_xor: int = 0) -> bytes:
    ends_xor &= 0xff
    _last = 0
    result = []
    for i in range(len(raw) - 1):
        result.append(raw[i] ^ raw[i + 1])
    result.append(raw[-1] ^ ends_xor)
    return bytes(result)


# To:
# x_0 ^ starts_xor, 
# (x_0 ^ x_1 ^ x_2), (x_2 ^ x_3 ^ x_4), ... , (x_(n-2) ^ x_(n-1) ^ x_n), 
# x_n ^ ends_xor
def bxorb_enc(raw: bytes, starts_xor: int = 0, ends_xor: int = 0) -> bytes:
    starts_xor &= 0xff
    ends_xor &= 0xff
    result = []
    result.append(raw[0] ^ starts_xor)
    for i in range(1, len(raw) - 1):
        result.append(raw[i - 1] ^ raw[i] ^ raw[i+1])
    result.append(raw[-1] ^ ends_xor)
    return bytes(result)

# WARNING: WRITING...
# # From:
# # x_0 ^ starts_xor, 
# # (x_0 ^ x_1 ^ x_2), (x_2 ^ x_3 ^ x_4), ... , (x_(n-2) ^ x_(n-1) ^ x_n), 
# # x_n ^ ends_xor
# from z3 import BitVec, Solver
# from copy import deepcopy
# def bxorb_dec(encoded: bytes, starts_xor: int = 0, ends_xor: int = 0) -> bytes:
#     if len(encoded) < 2:
#         return b''
#     result = []
#     x = [BitVec(f"x{i}", 8) for i in range(len(encoded))]
#     y = deepcopy(x)
#     s = Solver()

#     for i in range(len(encoded)):
        
