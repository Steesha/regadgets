from typing import List, Iterator
def rc4_init(key: bytes, box_size: int = 256) -> List[int]:
    if type(key) == str:
        key = key.encode()
    s = list(range(box_size))
    j = 0
    key_length = len(key)

    # Key scheduling algorithm (KSA)
    for i in range(box_size):
        # permit key is empty.
        j = (j + s[i] + 0 if key_length == 0 else j + s[i] + key[i % key_length]) % box_size
        # Swap s[i], s[j]
        s[i], s[j] = s[j], s[i]

    return s

def rc4_crypt(s: bytes, data: bytes, box_size: int = 256) -> bytes:
    i, j = 0, 0
    result = bytearray()

    # Pseudo-random generation algorithm (PRGA)
    for k in range(len(data)):
        i = (i + 1) %  box_size
        j = (j + s[i]) % box_size

        # Swap s[i], s[j]
        s[i], s[j] = s[j], s[i]

        t = (s[i] + s[j]) % box_size
        result.append(data[k] ^ s[t])

    return bytes(result)

def rc4_keystream(s: bytes, buf_len: int, box_size: int = 256)-> Iterator[int]:
    i, j = 0, 0
    # Generate the keystream
    for _ in range(buf_len):
        i = (i + 1) % box_size
        j = (j + s[i]) % box_size

        # Swap s[i], s[j]
        s[i], s[j] = s[j], s[i]

        t = (s[i] + s[j]) % box_size
        yield s[t]
