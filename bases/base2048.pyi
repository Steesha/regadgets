"""Binary encoding using Base2048"""

class DecodeError(ValueError):
    """Base2048 decoding error"""

def encode(s: bytes) -> str:
    """
    Encode a bytes-like object s using Base2048 and returns a string.

    Args:
        s: Bytes-like object to encode.

    Returns:
        str: Encoded string.
    """

def decode(s: str) -> bytes:
    """
    Decodes a string s using Base2048.

    Args:
        s: string to decode.

    Returns:
        bytes: Decoded bytes.
    """
