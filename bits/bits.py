def ror8(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xFF
def rol8(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xFF

def rol16(x, n):
    return ((x << n) | (x >> (16 - n))) & 0xFFFF
def ror16(x, n):
    return ((x >> n) | (x << (16 - n))) & 0xFFFF

def rol32(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
def ror32(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def rol64(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF
def ror64(x, n):
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF