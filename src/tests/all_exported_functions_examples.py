"""
Quick reference for all top-level exported functions in `regadgets`.

This file is meant to be read and copied from, not executed end-to-end.
Some examples depend on optional packages or specific runtime contexts.
"""

from ctypes import c_uint32

import regadgets as rg


def bases_examples():
    raw = b"flag{demo}"

    b16 = rg.encode_b16(raw)
    raw = rg.decode_b16(b16)

    b32 = rg.encode_b32(raw)
    raw = rg.decode_b32(b32)

    b45 = rg.encode_b45(raw)
    raw = rg.decode_b45(b45)

    b58 = rg.encode_b58(raw)
    raw = rg.decode_b58(b58)

    b62 = rg.encode_b62(raw)
    raw = rg.decode_b62(b62)

    b64 = rg.encode_b64(raw)
    raw = rg.decode_b64(b64)

    b85 = rg.encode_b85(raw)
    raw = rg.decode_b85(b85)

    b91 = rg.encode_b91(raw)
    raw = rg.decode_b91(b91)

    b92 = rg.encode_b92(raw)
    raw = rg.decode_b92(b92)

    # Requires the optional `base2048` dependency:
    # b2048 = rg.encode_b2048(raw)
    # raw = rg.decode_b2048(b2048)


def bits_examples():
    v8 = rg.rol8(0x81, 1)
    v8 = rg.ror8(v8, 1)

    v16 = rg.rol16(0x1234, 4)
    v16 = rg.ror16(v16, 4)

    v32 = rg.rol32(0x12345678, 8)
    v32 = rg.ror32(v32, 8)

    v64 = rg.rol64(0x0123456789ABCDEF, 16)
    v64 = rg.ror64(v64, 16)

    dwords = rg.byte2dword(b"\x12\x34\x56\x78", "big")
    raw = rg.dword2byte(dwords)

    words = rg.byte2word(b"\x12\x34", "big")
    raw = rg.word2byte(words)

    qwords = rg.byte2qword(b"\x01\x02\x03\x04\x05\x06\x07\x08", "big")
    raw = rg.qword2byte(qwords)

    tuples = list(rg.pack_dword([1, 2, 3, 4], crows=2))
    flat = rg.unpack_dword(tuples)

    swapped = rg.bswap32([0x12345678, 0xAABBCCDD])
    value = rg.b2l(b"\x01\x00")
    raw = rg.l2b(value, 2)

    floats = rg.byte2float(b"\x00\x00\x80\x3f")
    doubles = rg.byte2double(b"\x00\x00\x00\x00\x00\x00\xf0\x3f")

    raw = rg.u82byte([0x41, 0x42, 0x143])
    c_arr = rg.cstyle_arr32([0x12345678, 0x90ABCDEF])


def crypto_examples():
    key16 = b"0123456789ABCDEF"
    key32 = b"0123456789ABCDEF0123456789ABCDEF"
    iv16 = b"init-vector-1234"
    stream = b"hello crypto world"
    block16x2 = b"0123456789ABCDEF0123456789ABCDEF"

    s = rg.rc4_init(b"Key")
    cipher = rg.rc4_crypt(s, b"Plaintext", modify_sbox=False)
    plain = rg.rc4_crypt(rg.rc4_init(b"Key"), cipher, modify_sbox=False)
    ks = list(rg.rc4_keystream(rg.rc4_init(b"Key"), 8, modify_sbox=False))

    bx1 = rg.bxorr_enc(b"ABCDE")
    bx2 = rg.bxorr_dec(bx1)
    bx3 = rg.bxorl_enc(b"ABCDE")
    bx4 = rg.bxorl_dec(bx3)
    bx5 = rg.bxor(b"\x01\x02", b"\x03\x04")
    bx6 = rg.bxor_cycle(b"hello", b"xy")

    tea_ct = rg.tea_encrypt(b"ABCDEFGH", key16)
    tea_pt = rg.tea_decrypt(tea_ct, key16)

    xtea_ct = rg.xtea_encrypt(b"ABCDEFGH", key16)
    xtea_pt = rg.xtea_decrypt(xtea_ct, key16)

    rc5_ct = rg.rc5_encrypt(b"ABCDEFGH", key16)
    rc5_pt = rg.rc5_decrypt(rc5_ct, key16)

    xxtea_ct = rg.xxtea_encrypt(b"0123456789ABCDEF", key16)
    xxtea_pt = rg.xxtea_decrypt(xxtea_ct, key16)
    shift1 = rg.xxtea_std_shift(c_uint32(1), c_uint32(2), c_uint32(3), [c_uint32(4)] * 4, 0)
    shift2 = rg.xxtea_ciscn2024_shift(c_uint32(1), c_uint32(2), c_uint32(3), [c_uint32(4)] * 4, 0)

    aes_obj = rg.AES(key16)
    aes_ecb = rg.AES_ecb_encrypt(block16x2, key16)
    aes_ecb_plain = rg.AES_ecb_decrypt(aes_ecb, key16)

    aes_cbc = rg.AES_cbc_encrypt(stream, key16, iv16)
    aes_cbc_plain = rg.AES_cbc_decrypt(aes_cbc, key16, iv16)

    aes_pcbc = rg.AES_pcbc_encrypt(stream, key16, iv16)
    aes_pcbc_plain = rg.AES_pcbc_decrypt(aes_pcbc, key16, iv16)

    aes_cfb = rg.AES_cfb_encrypt(stream, key16, iv16)
    aes_cfb_plain = rg.AES_cfb_decrypt(aes_cfb, key16, iv16)

    aes_ofb = rg.AES_ofb_encrypt(stream, key16, iv16)
    aes_ofb_plain = rg.AES_ofb_decrypt(aes_ofb, key16, iv16)

    aes_ctr = rg.AES_ctr_encrypt(stream, key16, iv16)
    aes_ctr_plain = rg.AES_ctr_decrypt(aes_ctr, key16, iv16)

    aes128_ecb = rg.AES128_ecb_encrypt(block16x2, key16)
    aes128_ecb_plain = rg.AES128_ecb_decrypt(aes128_ecb, key16)
    aes128_cbc = rg.AES128_cbc_encrypt(stream, key16, iv16)
    aes128_cbc_plain = rg.AES128_cbc_decrypt(aes128_cbc, key16, iv16)
    aes128_pcbc = rg.AES128_pcbc_encrypt(stream, key16, iv16)
    aes128_pcbc_plain = rg.AES128_pcbc_decrypt(aes128_pcbc, key16, iv16)
    aes128_cfb = rg.AES128_cfb_encrypt(stream, key16, iv16)
    aes128_cfb_plain = rg.AES128_cfb_decrypt(aes128_cfb, key16, iv16)
    aes128_ofb = rg.AES128_ofb_encrypt(stream, key16, iv16)
    aes128_ofb_plain = rg.AES128_ofb_decrypt(aes128_ofb, key16, iv16)
    aes128_ctr = rg.AES128_ctr_encrypt(stream, key16, iv16)
    aes128_ctr_plain = rg.AES128_ctr_decrypt(aes128_ctr, key16, iv16)

    aes256_ecb = rg.AES256_ecb_encrypt(block16x2, key32)
    aes256_ecb_plain = rg.AES256_ecb_decrypt(aes256_ecb, key32)
    aes256_cbc = rg.AES256_cbc_encrypt(stream, key32, iv16)
    aes256_cbc_plain = rg.AES256_cbc_decrypt(aes256_cbc, key32, iv16)
    aes256_pcbc = rg.AES256_pcbc_encrypt(stream, key32, iv16)
    aes256_pcbc_plain = rg.AES256_pcbc_decrypt(aes256_pcbc, key32, iv16)
    aes256_cfb = rg.AES256_cfb_encrypt(stream, key32, iv16)
    aes256_cfb_plain = rg.AES256_cfb_decrypt(aes256_cfb, key32, iv16)
    aes256_ofb = rg.AES256_ofb_encrypt(stream, key32, iv16)
    aes256_ofb_plain = rg.AES256_ofb_decrypt(aes256_ofb, key32, iv16)
    aes256_ctr = rg.AES256_ctr_encrypt(stream, key32, iv16)
    aes256_ctr_plain = rg.AES256_ctr_decrypt(aes256_ctr, key32, iv16)

    aes_helper_ct = rg.aes_encrypt("hello", "30313233343536373839414243444546", mode="cfb", iv="init-vector-1234", key_format="hex", data_format="text")
    aes_helper_pt = rg.aes_decrypt(aes_helper_ct, "30313233343536373839414243444546", mode="cfb", iv="init-vector-1234", key_format="hex")

    bf = rg.BlowFish(b"BlowfishKey")
    sm4_block = rg.SM4_encrypt(0x0123456789ABCDEFFEDCBA9876543210, 0x0123456789ABCDEFFEDCBA9876543210)
    sm4_plain = rg.SM4_decrypt(sm4_block, 0x0123456789ABCDEFFEDCBA9876543210)
    sm4_ecb = rg.SM4_encrypt_ecb(b"hello-sm4", b"0123456789abcde")
    sm4_ecb_plain = rg.SM4_decrypt_ecb(sm4_ecb, b"0123456789abcde")
    sm4_cbc = rg.SM4_encrypt_cbc(b"hello-sm4", b"0123456789abcde", b"1234567890abcde")
    sm4_cbc_plain = rg.SM4_decrypt_cbc(sm4_cbc, b"0123456789abcde", b"1234567890abcde")


def transform_examples():
    s_box, inv_sbox = rg.generate_sbox(b"abcd", b"bcda")
    transformed = rg.sbox_transform(b"abcd", s_box)


def bruteforce_examples():
    result = rg.rg_brute_forcer(
        b"gm`fze",
        max_depth=1,
        methods=[lambda data, key=1: bytes([i ^ key for i in data])],
        predicate=lambda data: b"flag" in data,
        verbose=False,
    )


def utils_examples():
    # Requires z3:
    # from z3 import BitVec, Solver
    # x = BitVec("x", 8)
    # s = Solver()
    # s.add(x < 3)
    # models = list(rg.z3_get_models(s))
    pass


def math_examples():
    dct_vals = rg.dct_transform([1.0, 2.0, 3.0, 4.0])
    idct_vals = rg.idct_transform(dct_vals)

    product = rg.matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    inverse = rg.matrix_inverse([[4.0, 7.0], [2.0, 6.0]])
    determinant = rg.matrix_determinant([[4, 7], [2, 6]])
    matrix = rg.generate_matrix_square([1, 2, 3, 4], 2)
    flat = rg.flat_matrix(matrix)


def random_examples():
    glibc_rng = rg.GLIBCRand(1)
    glibc_one = glibc_rng.rand()
    glibc_many = glibc_rng.rands(5)

    windows_rng = rg.WindowsRand(1)
    windows_one = windows_rng.rand()
    windows_many = windows_rng.rands(5)


if __name__ == "__main__":
    print("Open this file and copy the example you need.")
