import time
import string
from typing import Callable, Iterable, Optional

from ..bits import rol8

def xor_decrypt(data: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in data])

def mod_add_decrypt(data: bytes, key: int) -> bytes:
    return bytes([(b + key) % 256 for b in data])

def mod_mul(data: bytes, key: int) -> bytes:
    return bytes([(b * key) % 256 for b in data])

def mod_rol(data: bytes, key: int) -> bytes:
    return bytes([rol8(b, key) % 256 for b in data])

permit = string.printable
permit = list(permit.encode())

def contains_target(data: bytes, target: bytes = b'flag{', permitted: Optional[Iterable[int]] = None) -> bool:
    if target not in data:
        return False
    permitted_bytes = permit if permitted is None else list(permitted)
    return all(i in permitted_bytes for i in data)


def _normalize_data(data):
    if isinstance(data, list):
        return bytes(data)
    if isinstance(data, bytes):
        return data
    raise TypeError("Input data should be bytes or list[int]")


def _is_printable_ascii(data: bytes) -> bool:
    return all(0x20 <= i <= 0x7F for i in data)


def _iter_method_results(data: bytes, method: Callable):
    if method in (xor_decrypt, mod_add_decrypt, mod_mul):
        for key in range(256):
            yield method(data, key), (method.__name__, key)
    elif method == mod_rol:
        for key in range(8):
            yield method(data, key), (method.__name__, key)
    else:
        yield method(data), method.__name__


def decrypt_recursive(
    data: bytes,
    depth: int,
    methods: list,
    path: list = None,
    predicate: Callable[[bytes], bool] = contains_target,
    ascii_prune_depth: Optional[int] = 1,
):
    data = _normalize_data(data)
    if path is None:
        path = []

    if depth == 0:
        if predicate(data):
            return {"path": path, "data": data}
        return None

    level = len(path) + 1
    for method in methods:
        for new_data, step in _iter_method_results(data, method):
            if ascii_prune_depth is not None and level == ascii_prune_depth and not _is_printable_ascii(new_data):
                continue
            result = decrypt_recursive(
                new_data,
                depth - 1,
                methods,
                path + [step],
                predicate=predicate,
                ascii_prune_depth=ascii_prune_depth,
            )
            if result is not None:
                return result

    return None


def rg_brute_forcer(
    data: bytes,
    max_depth: int,
    methods: Optional[list] = None,
    predicate: Callable[[bytes], bool] = contains_target,
    ascii_prune_depth: Optional[int] = 1,
    verbose: bool = False,
):
    data = _normalize_data(data)
    methods = [xor_decrypt, mod_add_decrypt, mod_mul, mod_rol] if methods is None else methods

    for depth in range(1, max_depth + 1):
        start_time = time.time()
        result = decrypt_recursive(
            data,
            depth,
            methods,
            predicate=predicate,
            ascii_prune_depth=ascii_prune_depth,
        )
        elapsed = time.time() - start_time
        if result is not None:
            result["depth"] = depth
            result["elapsed"] = elapsed
            if verbose:
                print(f"[success] found chain at depth {depth} in {elapsed:.6f}s")
                print(f"path: {result['path']}")
                print(f"data: {result['data']}")
            return result
        if verbose:
            print(f"[miss] no chain at depth {depth} in {elapsed:.6f}s")
    if verbose:
        print("no valid decryption chain found")
    return None
