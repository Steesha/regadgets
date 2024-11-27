import base64
from .base45 import b45decode, b45encode
from .base62 import  encodebytes as b62encode, decodebytes as b62decode
from .base58 import b58decode, b58encode, BITCOIN_ALPHABET as B58_BITCOIN_ALPHABET
from .base91 import decode as b91decode, encode as b91encode
from .py3base92 import b92decode, b92encode
from base2048 import decode as b2048decode, encode as b2048encode
from .base65536 import decode as b65536decode, encode as b65536encode

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
    return b45decode(encoded)

def encode_b45(raw: bytes, table: str = "") -> str:
    result = b45encode(raw).decode()
    table = BASE45_STD_TABLE if table == "" else table
    result = str_trans(result, BASE45_STD_TABLE, table)
    return result

def decode_b62(encoded: str, table: str = "") -> bytes:
    table = BASE62_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE62_STD_TABLE)
    return b62decode.decodebytes(encoded)

def encode_b62(raw: bytes, table: str = "") -> str:
    result = b62encode.encodebytes(raw)
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


def decode_b58(encoded: str, table: str = B58_BITCOIN_ALPHABET) -> bytes:
    return b58decode(encoded, table)

def encode_b58(raw: bytes, table: str = B58_BITCOIN_ALPHABET) -> str:
    return b58encode(raw, table).decode('utf-8')


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
    return bytes(b91decode(encoded))

def encode_b91(raw: bytes, table: str = "") -> str:
    result = b91encode(raw)
    table = BASE91_STD_TABLE if table == "" else table
    result = str_trans(result, BASE91_STD_TABLE, table)
    return result


def decode_b92(encoded: str, table: str = "") -> bytes:
    table = BASE92_STD_TABLE if table == "" else table
    encoded = str_trans(encoded, table, BASE92_STD_TABLE)
    return b92decode(encoded)

def encode_b92(raw: bytes, table: str = "") -> str:
    result = b92encode(raw)
    table = BASE92_STD_TABLE if table == "" else table
    result = str_trans(result, BASE92_STD_TABLE, table)
    return result

def encode_b2048(raw: bytes) -> str:
    return b2048encode(raw)

def decode_b2048(encoded: str) -> bytes:
    return b2048decode(encoded)

def encode_b65536(raw: bytes) -> str:
    return b65536encode(raw)

def decode_b65536(encoded: str) -> bytes:
    return b65536decode(encoded)
