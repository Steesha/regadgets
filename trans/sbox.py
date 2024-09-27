from typing import List, Tuple


# retval: (sbox, inv_sbox)
def generate_sbox(_from: bytes | List[int], _to: bytes | List[int]) -> Tuple[List[int], List[int]]:
    inv_sbox = [_to.index(i) for i in _from]
    s_box = [_from.index(i) for i in _to]
    return s_box, inv_sbox


def sbox_transform(_from: bytes | List[int], box: List[int]):
    r = [_from[box[i]] for i in range(len(_from))]
    if type(_from) == bytes:
        return bytes(r)
    else:
        return r
