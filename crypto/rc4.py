from typing import List
def rc4_init(key: bytes) -> List[int]:
    s = list(range(256))
    j = 0
    key_length = len(key)

    # Key scheduling algorithm (KSA)
    for i in range(256):
        # permit key is empty.
        j = (j + s[i] + 0 if key_length == 0 else key[i % key_length]) % 256
        # Swap s[i], s[j]
        s[i], s[j] = s[j], s[i]

    return s

def rc4_crypt(s: bytes, data: bytes) -> bytes:
    i = 0
    j = 0
    result = bytearray()

    # Pseudo-random generation algorithm (PRGA)
    for k in range(len(data)):
        i = (i + 1) % 256
        j = (j + s[i]) % 256

        # Swap s[i], s[j]
        s[i], s[j] = s[j], s[i]

        t = (s[i] + s[j]) % 256
        result.append(data[k] ^ s[t])

    return bytes(result)

def rc4_keystream(s: bytes, buf_len: int) -> List[int]:
    i = 0
    j = 0
    keystream = bytearray()

    # Generate the keystream
    for k in range(buf_len):
        i = (i + 1) % 256
        j = (j + s[i]) % 256

        # Swap s[i], s[j]
        s[i], s[j] = s[j], s[i]

        t = (s[i] + s[j]) % 256
        keystream.append(s[t])

    return keystream
