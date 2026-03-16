import unittest


class RegadgetsSmokeTests(unittest.TestCase):
    def test_top_level_import_without_base2048(self):
        import regadgets

        self.assertTrue(hasattr(regadgets, "encode_b16"))
        self.assertTrue(hasattr(regadgets, "rol32"))

    def test_common_base_encoders_roundtrip(self):
        from regadgets.bases.bases import decode_b16, decode_b32, encode_b16, encode_b32

        raw = b"flag{smoke}"
        self.assertEqual(encode_b16(raw), "666C61677B736D6F6B657D")
        self.assertEqual(decode_b16("666C61677B736D6F6B657D"), raw)
        self.assertEqual(encode_b32(raw), "MZWGCZ33ONWW623FPU======")
        self.assertEqual(decode_b32("MZWGCZ33ONWW623FPU======"), raw)

    def test_base2048_functions_fail_lazily_without_dependency(self):
        from regadgets.bases.bases import decode_b2048, encode_b2048

        with self.assertRaises(ImportError):
            encode_b2048(b"abc")
        with self.assertRaises(ImportError):
            decode_b2048("abc")

    def test_rotate_helpers(self):
        from regadgets.bits.bits import rol8, rol32, ror8, ror32

        self.assertEqual(rol8(0x81, 1), 0x03)
        self.assertEqual(ror8(0x03, 1), 0x81)
        self.assertEqual(rol32(0x12345678, 8), 0x34567812)
        self.assertEqual(ror32(0x12345678, 8), 0x78123456)

    def test_endian_helpers(self):
        from regadgets.bits.bits import byte2dword, byte2qword, byte2word, qword2byte

        self.assertEqual(byte2word([0x12, 0x34], "big"), [0x1234])
        self.assertEqual(byte2word([0x12, 0x34], "little"), [0x3412])
        self.assertEqual(byte2dword([0x12, 0x34, 0x56, 0x78], "big"), [0x12345678])
        self.assertEqual(byte2qword([1, 2, 3, 4, 5, 6, 7, 8], "big"), [0x0102030405060708])
        self.assertEqual(qword2byte([0x0102030405060708]), b"\x08\x07\x06\x05\x04\x03\x02\x01")

    def test_matrix_inverse_does_not_mutate_input(self):
        from regadgets.math.matrix import matrix_inverse

        matrix = [[4.0, 7.0], [2.0, 6.0]]
        snapshot = [row[:] for row in matrix]
        inverse = matrix_inverse(matrix)

        self.assertEqual(matrix, snapshot)
        self.assertAlmostEqual(inverse[0][0], 0.6)
        self.assertAlmostEqual(inverse[0][1], -0.7)
        self.assertAlmostEqual(inverse[1][0], -0.2)
        self.assertAlmostEqual(inverse[1][1], 0.4)

    def test_generate_matrix_square_validates_shape(self):
        from regadgets.math.matrix import generate_matrix_square

        self.assertEqual(generate_matrix_square([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            generate_matrix_square([1, 2, 3], 2)

    def test_bruteforcer_returns_result_without_printing(self):
        from regadgets.bruteforce.bruteforcer import contains_target, rg_brute_forcer, xor_decrypt

        plaintext = b"flag{demo}"
        ciphertext = xor_decrypt(plaintext, 1)

        result = rg_brute_forcer(
            ciphertext,
            1,
            methods=[xor_decrypt],
            predicate=lambda data: contains_target(data, target=b"flag{demo}"),
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["data"], plaintext)
        self.assertEqual(result["path"], [("xor_decrypt", 1)])
        self.assertEqual(result["depth"], 1)

    def test_aes_five_modes_roundtrip_for_128_and_256(self):
        from regadgets.crypto import (
            AES128_cbc_decrypt,
            AES128_cbc_encrypt,
            AES128_cfb_decrypt,
            AES128_cfb_encrypt,
            AES128_ctr_decrypt,
            AES128_ctr_encrypt,
            AES128_ecb_decrypt,
            AES128_ecb_encrypt,
            AES128_ofb_decrypt,
            AES128_ofb_encrypt,
            AES256_cbc_decrypt,
            AES256_cbc_encrypt,
            AES256_cfb_decrypt,
            AES256_cfb_encrypt,
            AES256_ctr_decrypt,
            AES256_ctr_encrypt,
            AES256_ecb_decrypt,
            AES256_ecb_encrypt,
            AES256_ofb_decrypt,
            AES256_ofb_encrypt,
        )

        block_plaintext = b"0123456789ABCDEF0123456789ABCDEF"
        stream_plaintext = b"stream-mode plaintext"
        iv = b"init-vector-1234"
        key128 = b"0123456789ABCDEF"
        key256 = b"0123456789ABCDEF0123456789ABCDEF"

        self.assertEqual(AES128_ecb_decrypt(AES128_ecb_encrypt(block_plaintext, key128), key128), block_plaintext)
        self.assertEqual(AES128_cbc_decrypt(AES128_cbc_encrypt(stream_plaintext, key128, iv), key128, iv), stream_plaintext)
        self.assertEqual(AES128_cfb_decrypt(AES128_cfb_encrypt(stream_plaintext, key128, iv), key128, iv), stream_plaintext)
        self.assertEqual(AES128_ofb_decrypt(AES128_ofb_encrypt(stream_plaintext, key128, iv), key128, iv), stream_plaintext)
        self.assertEqual(AES128_ctr_decrypt(AES128_ctr_encrypt(stream_plaintext, key128, iv), key128, iv), stream_plaintext)

        self.assertEqual(AES256_ecb_decrypt(AES256_ecb_encrypt(block_plaintext, key256), key256), block_plaintext)
        self.assertEqual(AES256_cbc_decrypt(AES256_cbc_encrypt(stream_plaintext, key256, iv), key256, iv), stream_plaintext)
        self.assertEqual(AES256_cfb_decrypt(AES256_cfb_encrypt(stream_plaintext, key256, iv), key256, iv), stream_plaintext)
        self.assertEqual(AES256_ofb_decrypt(AES256_ofb_encrypt(stream_plaintext, key256, iv), key256, iv), stream_plaintext)
        self.assertEqual(AES256_ctr_decrypt(AES256_ctr_encrypt(stream_plaintext, key256, iv), key256, iv), stream_plaintext)

    def test_aes_key_size_helpers_validate_lengths(self):
        from regadgets.crypto import AES128_cbc_encrypt, AES256_cbc_encrypt

        with self.assertRaises(ValueError):
            AES128_cbc_encrypt(b"hello", b"short", b"init-vector-1234")
        with self.assertRaises(ValueError):
            AES256_cbc_encrypt(b"hello", b"0123456789ABCDEF", b"init-vector-1234")

    def test_aes_pcbc_roundtrip(self):
        from regadgets.crypto import AES128_pcbc_decrypt, AES128_pcbc_encrypt

        plaintext = b"pcbc example payload"
        key = b"0123456789ABCDEF"
        iv = b"init-vector-1234"

        ciphertext = AES128_pcbc_encrypt(plaintext, key, iv)
        self.assertEqual(AES128_pcbc_decrypt(ciphertext, key, iv), plaintext)

    def test_aes_helpers_accept_hex_and_text_inputs(self):
        from regadgets.crypto import aes_decrypt, aes_encrypt

        plaintext = "stream helper"
        key_hex = "30313233343536373839414243444546"
        iv_text = "init-vector-1234"

        ciphertext = aes_encrypt(plaintext, key_hex, mode="cfb", iv=iv_text, key_format="hex", data_format="text")
        recovered = aes_decrypt(ciphertext, key_hex, mode="cfb", iv=iv_text, key_format="hex")

        self.assertEqual(recovered, plaintext.encode("utf-8"))

    def test_aes_helper_requires_iv_for_stateful_modes(self):
        from regadgets.crypto import aes_encrypt

        with self.assertRaises(ValueError):
            aes_encrypt(b"abc", b"0123456789ABCDEF", mode="cbc")


if __name__ == "__main__":
    unittest.main()
