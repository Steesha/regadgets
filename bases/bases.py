import base64
import regadgets.bases.base58 as base58
import regadgets.bases.base91 as base91
import regadgets.bases.py3base92 as py3base92
import regadgets.bases.base62 as base62
import regadgets.bases.base45 as base45
import regadgets.bases.base2048 as base2048
import regadgets.bases.base65536 as base65536

from typing import List

BASE16_STD_TABLE = r"0123456789ABCDEF"
BASE32_STD_TABLE = r"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
BASE45_STD_TABLE = r'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"'
BASE58_STD_TABLE = r"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE62_STD_TABLE = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE64_STD_TABLE = r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
BASE85_STD_TABLE = r'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
BASE91_STD_TABLE = r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'
BASE92_STD_TABLE = r"!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}"

def str_trans(raw: str, from_table: str, to_table: str) -> str:
    if from_table == to_table:
        return raw
    if len(from_table) == len(to_table) - 1:
        from_table += '='
    trans = str.maketrans(from_table, to_table)
    return raw.translate(trans)

def decode_b16(encoded: str, table: str = "") -> bytes:
    table = BASE16_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE16_STD_TABLE)
    return base64.b16decode(encoded)

def encode_b16(raw: bytes, table: str = "") -> str:
    result = base64.b16encode(raw)
    table = BASE16_STD_TABLE if table == "" else table
    result = str_trans(result, BASE16_STD_TABLE, table)
    return result

def decode_b32(encoded: str, table: str = "") -> bytes:
    table = BASE32_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE32_STD_TABLE)
    return base64.b32decode(encoded)
def encode_b32(raw: bytes, table: str = "") -> str:
    result = base64.b32encode(raw)
    table = BASE32_STD_TABLE if table == "" else table
    result = str_trans(result, BASE32_STD_TABLE, table)
    return result

def decode_b45(encoded: str, table: str = "") -> bytes:
    table = BASE45_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE45_STD_TABLE)
    return base45.b45decode(encoded)

def encode_b45(raw: bytes, table: str = "") -> str:
    result = base45.b45encode(raw).decode()
    table = BASE45_STD_TABLE if table == "" else table
    result = str_trans(result, BASE45_STD_TABLE, table)
    return result

def decode_b62(encoded: str, table: str = "") -> bytes:
    table = BASE62_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE62_STD_TABLE)
    return base62.decodebytes(encoded)

def encode_b62(raw: bytes, table: str = "") -> str:
    result = base62.encodebytes(raw)
    table = BASE62_STD_TABLE if table == "" else table
    result = str_trans(result, BASE62_STD_TABLE, table)
    return result

def decode_b64(encoded: str, table: str = "") -> bytes:
    table = BASE64_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE64_STD_TABLE)
    return base64.b64decode(encoded)

def encode_b64(raw: bytes, table: str = "") -> str:
    result = base64.b64encode(raw).decode('utf-8')
    table = BASE64_STD_TABLE if table == "" else table
    result = str_trans(result, BASE64_STD_TABLE, table)
    return result


def decode_b58(encoded: str, table: str = base58.BITCOIN_ALPHABET) -> bytes:
    return base58.b58decode(encoded, table)

def encode_b58(raw: bytes, table: str = base58.BITCOIN_ALPHABET) -> str:
    return base58.b58encode(raw, table).decode('utf-8')


def decode_b85(encoded: str, table: str = "") -> bytes:
    table = BASE85_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE85_STD_TABLE)
    return base64.b85decode(encoded)

def encode_b85(raw: bytes, table: str = "") -> str:
    result = base64.b85encode(raw, False).decode('utf-8')
    table = BASE85_STD_TABLE if table == "" else table
    result = str_trans(result, BASE85_STD_TABLE, table)
    return result

def decode_b91(encoded: str, table: str = "") -> bytes:
    table = BASE91_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE91_STD_TABLE)
    return bytes(base91.decode(encoded))

def encode_b91(raw: bytes, table: str = "") -> str:
    result = base91.encode(raw)
    table = BASE91_STD_TABLE if table == "" else table
    result = str_trans(result, BASE91_STD_TABLE, table)
    return result


def decode_b92(encoded: str, table: str = "") -> bytes:
    table = BASE92_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE92_STD_TABLE)
    return py3base92.b92decode(encoded)

def encode_b92(raw: bytes, table: str = "") -> str:
    result = py3base92.b92encode(raw)
    table = BASE92_STD_TABLE if table == "" else table
    result = str_trans(result, BASE92_STD_TABLE, table)
    return result

def encode_b2048(raw: bytes) -> str:
    return base2048.encode(raw)

def decode_b2048(encoded: str) -> bytes:
    return base2048.decode(encoded)

def encode_b65536(raw: bytes) -> str:
    return base65536.encode(raw)

def decode_b65536(encoded: str) -> bytes:
    return base65536.decode(encoded)
