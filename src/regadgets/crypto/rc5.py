from typing import List, Tuple, Union


RC5_CONSTANTS = {
    16: (0xB7E1, 0x9E37),
    32: (0xB7E15163, 0x9E3779B9),
    64: (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15),
}


def _rol(value: int, shift: int, word_size: int) -> int:
    mask = (1 << word_size) - 1
    shift &= word_size - 1
    return ((value << shift) | (value >> (word_size - shift))) & mask


def _ror(value: int, shift: int, word_size: int) -> int:
    mask = (1 << word_size) - 1
    shift &= word_size - 1
    return ((value >> shift) | (value << (word_size - shift))) & mask


def _validate_word_size(word_size: int):
    if word_size not in RC5_CONSTANTS:
        raise ValueError("word_size must be one of 16, 32, or 64")


def _word_bytes(word_size: int) -> int:
    _validate_word_size(word_size)
    return word_size // 8


def _key_to_bytes(key: Union[List[int], bytes], word_size: int) -> bytes:
    if isinstance(key, bytes):
        return key
    if isinstance(key, list):
        word_bytes = _word_bytes(word_size)
        try:
            return b"".join(int(i).to_bytes(word_bytes, "little", signed=False) for i in key)
        except OverflowError as exc:
            raise ValueError("key list values must fit within the configured word size") from exc
    raise TypeError("wrong key type")


def _expand_key(key: Union[List[int], bytes], rounds: int, word_size: int) -> List[int]:
    key_bytes = _key_to_bytes(key, word_size)
    word_bytes = _word_bytes(word_size)
    mask = (1 << word_size) - 1
    pw, qw = RC5_CONSTANTS[word_size]

    c = max(1, (len(key_bytes) + word_bytes - 1) // word_bytes)
    l_words = [0] * c
    for i in range(len(key_bytes) - 1, -1, -1):
        l_words[i // word_bytes] = ((l_words[i // word_bytes] << 8) + key_bytes[i]) & mask

    t = 2 * (rounds + 1)
    s_words = [0] * t
    s_words[0] = pw
    for i in range(1, t):
        s_words[i] = (s_words[i - 1] + qw) & mask

    a = b = i = j = 0
    for _ in range(3 * max(c, t)):
        a = s_words[i] = _rol((s_words[i] + a + b) & mask, 3, word_size)
        b = l_words[j] = _rol((l_words[j] + a + b) & mask, (a + b) & (word_size - 1), word_size)
        i = (i + 1) % t
        j = (j + 1) % c
    return s_words


def _tuple_to_bytes(block: Tuple[int, int], word_size: int) -> bytes:
    word_bytes = _word_bytes(word_size)
    return block[0].to_bytes(word_bytes, "little") + block[1].to_bytes(word_bytes, "little")


def _bytes_to_words(src: bytes, word_size: int) -> List[int]:
    word_bytes = _word_bytes(word_size)
    if len(src) % word_bytes != 0:
        raise ValueError("src length must be a multiple of the word size in bytes")
    return [int.from_bytes(src[i:i + word_bytes], "little") for i in range(0, len(src), word_bytes)]


def rc5_encrypt(
    src: Union[Tuple[int, int], bytes, List[int]],
    key: Union[List[int], bytes],
    rounds: int = 12,
    word_size: int = 32,
) -> Union[Tuple[int, int], bytes]:
    mask = (1 << word_size) - 1
    s_words = _expand_key(key, rounds, word_size)

    if isinstance(src, bytes):
        words = _bytes_to_words(src, word_size)
        if len(words) % 2 != 0:
            raise ValueError("src length must be a multiple of the RC5 block size")
        result = b""
        for i in range(0, len(words), 2):
            result += _tuple_to_bytes(rc5_encrypt((words[i], words[i + 1]), key, rounds, word_size), word_size)
        return result
    if isinstance(src, list):
        if len(src) % 2 != 0:
            raise ValueError("src list length must be even")
        result = b""
        for i in range(0, len(src), 2):
            result += _tuple_to_bytes(rc5_encrypt((src[i], src[i + 1]), key, rounds, word_size), word_size)
        return result
    if not isinstance(src, tuple) or len(src) != 2:
        raise TypeError("wrong src type")

    a = (src[0] + s_words[0]) & mask
    b = (src[1] + s_words[1]) & mask
    for i in range(1, rounds + 1):
        a = (_rol(a ^ b, b, word_size) + s_words[2 * i]) & mask
        b = (_rol(b ^ a, a, word_size) + s_words[2 * i + 1]) & mask
    return (a, b)


def rc5_decrypt(
    src: Union[Tuple[int, int], bytes, List[int]],
    key: Union[List[int], bytes],
    rounds: int = 12,
    word_size: int = 32,
) -> Union[Tuple[int, int], bytes]:
    mask = (1 << word_size) - 1
    s_words = _expand_key(key, rounds, word_size)

    if isinstance(src, bytes):
        words = _bytes_to_words(src, word_size)
        if len(words) % 2 != 0:
            raise ValueError("src length must be a multiple of the RC5 block size")
        result = b""
        for i in range(0, len(words), 2):
            result += _tuple_to_bytes(rc5_decrypt((words[i], words[i + 1]), key, rounds, word_size), word_size)
        return result
    if isinstance(src, list):
        if len(src) % 2 != 0:
            raise ValueError("src list length must be even")
        result = b""
        for i in range(0, len(src), 2):
            result += _tuple_to_bytes(rc5_decrypt((src[i], src[i + 1]), key, rounds, word_size), word_size)
        return result
    if not isinstance(src, tuple) or len(src) != 2:
        raise TypeError("wrong src type")

    a, b = src
    for i in range(rounds, 0, -1):
        b = _ror((b - s_words[2 * i + 1]) & mask, a, word_size) ^ a
        a = _ror((a - s_words[2 * i]) & mask, b, word_size) ^ b
    b = (b - s_words[1]) & mask
    a = (a - s_words[0]) & mask
    return (a, b)
