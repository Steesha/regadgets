import time
import string
from regadgets.bits import rol8

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

def contains_target(data: bytes) -> bool:
    if b'flag{' not in data:
        return False
    return all([i in permit for i in data])

# 递归爆破解密，执行不同层次和排列组合的解密
def decrypt_recursive(data: bytes, depth: int, methods: list, path: list = None):
    if path is None:
        path = []

    if depth == 0:
        # 如果达到设定深度，检查是否包含目标字符串
        if contains_target(data):
            print(f"找到正确解密链: {path}")
            print(f"解密结果: {data}")
            return True
        return False

    # 遍历每种解密方法
    for _, method in enumerate(methods):
        if method == xor_decrypt:
            for key in range(256):
                new_data = method(data, key)
                if depth + 1 == len(path):
                    if not all([i >= 0x20 and i <= 0x7f for i in new_data]):
                        return False
                if decrypt_recursive(new_data, depth - 1, methods, path + [(method.__name__, key)]):
                    return True
        elif method == mod_add_decrypt:
             for key in range(256):
                new_data = method(data, key)
                if depth + 1 == len(path):
                    if not all([i >= 0x20 and i <= 0x7f for i in new_data]):
                        return False
                if decrypt_recursive(new_data, depth - 1, methods, path + [(method.__name__, key)]):
                    return True
        elif method == mod_mul:
             for key in range(256):
                new_data = method(data, key)
                if depth + 1 == len(path):
                    if not all([i >= 0x20 and i <= 0x7f for i in new_data]):
                        return False
                if decrypt_recursive(new_data, depth - 1, methods, path + [(method.__name__, key)]):
                    return True
        elif method == mod_rol:
             for key in range(8):
                new_data = method(data, key)
                if depth + 1 == len(path):
                    if not all([i >= 0x20 and i <= 0x7f for i in new_data]):
                        return False
                if decrypt_recursive(new_data, depth - 1, methods, path + [(method.__name__, key)]):
                    return True
        else:
            new_data = method(data)
            if decrypt_recursive(new_data, depth - 1, methods, path + [method.__name__]):
                return True

    return False

# 爆破函数：输入密文和最大深度，逐步递归尝试解密
def rg_brute_forcer(data: bytes, max_depth: int):
    if isinstance(data, list):
        data = bytes(data)
    elif not isinstance(data, bytes):
        raise "Input Data should be bytes | list"
    methods = [xor_decrypt, mod_add_decrypt, mod_mul, mod_rol]
    
    for depth in range(1, max_depth + 1):
        print(f"尝试深度 {depth} 的解密...")
        start_time = time.time()
        if decrypt_recursive(data, depth, methods):
            print(f"[成功] 在深度 {depth} 找到解密方案，用时 {time.time() - start_time}秒")
            return
        print(f"[失败] 没有在深度 {depth} 找到解密方案，用时 {time.time() - start_time}秒")
    print("未找到正确的解密链")