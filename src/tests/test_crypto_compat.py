import unittest


try:
    from Crypto.Cipher import AES as CryptoAES
    from Crypto.Cipher import ARC4, Blowfish as CryptoBlowfish
    from Crypto.Util import Counter
    from Crypto.Util.Padding import pad

    HAS_PYCRYPTODOME = True
except ImportError:
    HAS_PYCRYPTODOME = False


class CryptoCompatibilityTests(unittest.TestCase):
    @unittest.skipUnless(HAS_PYCRYPTODOME, "PyCryptodome is required for compatibility tests")
    def test_aes_128_matches_pycryptodome_in_common_modes(self):
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
        )

        key = b"0123456789ABCDEF"
        iv = b"init-vector-1234"
        aligned = b"0123456789ABCDEF0123456789ABCDEF"
        stream = b"AES-128 compatibility sample."

        self.assertEqual(
            AES128_ecb_encrypt(aligned, key),
            CryptoAES.new(key, CryptoAES.MODE_ECB).encrypt(aligned),
        )
        self.assertEqual(
            AES128_ecb_decrypt(AES128_ecb_encrypt(aligned, key), key),
            aligned,
        )

        self.assertEqual(
            AES128_cbc_encrypt(stream, key, iv),
            CryptoAES.new(key, CryptoAES.MODE_CBC, iv=iv).encrypt(pad(stream, 16)),
        )
        self.assertEqual(
            AES128_cbc_decrypt(AES128_cbc_encrypt(stream, key, iv), key, iv),
            stream,
        )

        cfb_expected = CryptoAES.new(key, CryptoAES.MODE_CFB, iv=iv, segment_size=128).encrypt(stream)
        self.assertEqual(AES128_cfb_encrypt(stream, key, iv), cfb_expected)
        self.assertEqual(AES128_cfb_decrypt(cfb_expected, key, iv), stream)

        ofb_expected = CryptoAES.new(key, CryptoAES.MODE_OFB, iv=iv).encrypt(stream)
        self.assertEqual(AES128_ofb_encrypt(stream, key, iv), ofb_expected)
        self.assertEqual(AES128_ofb_decrypt(ofb_expected, key, iv), stream)

        ctr_expected = CryptoAES.new(
            key,
            CryptoAES.MODE_CTR,
            nonce=b"",
            initial_value=int.from_bytes(iv, "big"),
        ).encrypt(stream)
        self.assertEqual(AES128_ctr_encrypt(stream, key, iv), ctr_expected)
        self.assertEqual(AES128_ctr_decrypt(ctr_expected, key, iv), stream)

    @unittest.skipUnless(HAS_PYCRYPTODOME, "PyCryptodome is required for compatibility tests")
    def test_aes_256_matches_pycryptodome_in_common_modes(self):
        from regadgets.crypto import (
            AES256_cbc_encrypt,
            AES256_cfb_encrypt,
            AES256_ctr_encrypt,
            AES256_ecb_encrypt,
            AES256_ofb_encrypt,
        )

        key = b"0123456789ABCDEF0123456789ABCDEF"
        iv = b"init-vector-1234"
        aligned = b"0123456789ABCDEF0123456789ABCDEF"
        stream = b"AES-256 compatibility sample."

        self.assertEqual(
            AES256_ecb_encrypt(aligned, key),
            CryptoAES.new(key, CryptoAES.MODE_ECB).encrypt(aligned),
        )
        self.assertEqual(
            AES256_cbc_encrypt(stream, key, iv),
            CryptoAES.new(key, CryptoAES.MODE_CBC, iv=iv).encrypt(pad(stream, 16)),
        )
        self.assertEqual(
            AES256_cfb_encrypt(stream, key, iv),
            CryptoAES.new(key, CryptoAES.MODE_CFB, iv=iv, segment_size=128).encrypt(stream),
        )
        self.assertEqual(
            AES256_ofb_encrypt(stream, key, iv),
            CryptoAES.new(key, CryptoAES.MODE_OFB, iv=iv).encrypt(stream),
        )
        self.assertEqual(
            AES256_ctr_encrypt(stream, key, iv),
            CryptoAES.new(key, CryptoAES.MODE_CTR, nonce=b"", initial_value=int.from_bytes(iv, "big")).encrypt(stream),
        )

    @unittest.skipUnless(HAS_PYCRYPTODOME, "PyCryptodome is required for compatibility tests")
    def test_blowfish_matches_pycryptodome_in_common_modes(self):
        from regadgets.crypto.blowfish import BlowFish

        key = b"BlowfishKey"
        iv = b"12345678"
        aligned = b"ABCDEFGHabcdefgh"
        stream = b"Blowfish stream sample."
        our = BlowFish(key)

        self.assertEqual(
            b"".join(our.encrypt_ecb(aligned)),
            CryptoBlowfish.new(key, CryptoBlowfish.MODE_ECB).encrypt(aligned),
        )
        self.assertEqual(
            b"".join(our.encrypt_cbc(aligned, iv)),
            CryptoBlowfish.new(key, CryptoBlowfish.MODE_CBC, iv=iv).encrypt(aligned),
        )
        self.assertEqual(
            b"".join(our.encrypt_cfb(stream, iv)),
            CryptoBlowfish.new(key, CryptoBlowfish.MODE_CFB, iv=iv, segment_size=64).encrypt(stream),
        )
        self.assertEqual(
            b"".join(our.encrypt_ofb(stream, iv)),
            CryptoBlowfish.new(key, CryptoBlowfish.MODE_OFB, iv=iv).encrypt(stream),
        )

        counter_start = int.from_bytes(iv, "big")
        counter_blocks = (len(stream) + 7) // 8
        our_ctr = b"".join(our.encrypt_ctr(stream, iter(range(counter_start, counter_start + counter_blocks))))
        ref_ctr = CryptoBlowfish.new(
            key,
            CryptoBlowfish.MODE_CTR,
            counter=Counter.new(64, initial_value=counter_start),
        ).encrypt(stream)
        self.assertEqual(our_ctr, ref_ctr)

    @unittest.skipUnless(HAS_PYCRYPTODOME, "PyCryptodome is required for compatibility tests")
    def test_rc4_matches_pycryptodome(self):
        from regadgets.crypto import rc4_crypt, rc4_init

        key = b"Key"
        plaintext = b"Plaintext"
        expected = ARC4.new(key).encrypt(plaintext)

        self.assertEqual(rc4_crypt(rc4_init(key), plaintext, modify_sbox=False), expected)
        self.assertEqual(rc4_crypt(rc4_init(key), expected, modify_sbox=False), plaintext)

    def test_sm4_roundtrip_is_consistent(self):
        from regadgets.crypto import SM4_decrypt_cbc, SM4_decrypt_ecb, SM4_encrypt_cbc, SM4_encrypt_ecb

        key = b"0123456789abcde"
        iv = b"1234567890abcde"
        plaintext = b"hello-sm4"

        ecb_cipher = SM4_encrypt_ecb(plaintext, key)
        ecb_plain = SM4_decrypt_ecb(ecb_cipher, key)
        if isinstance(ecb_plain, str):
            ecb_plain = ecb_plain.encode("utf-8")
        self.assertEqual(ecb_plain, plaintext)

        cbc_cipher = SM4_encrypt_cbc(plaintext, key, iv)
        cbc_plain = SM4_decrypt_cbc(cbc_cipher, key, iv)
        if isinstance(cbc_plain, str):
            cbc_plain = cbc_plain.encode("utf-8")
        self.assertEqual(cbc_plain, plaintext)

    def test_tea_family_roundtrip_is_consistent(self):
        from regadgets.crypto import rc5_decrypt, rc5_encrypt, tea_decrypt, tea_encrypt, xtea_decrypt, xtea_encrypt, xxtea_decrypt, xxtea_encrypt

        key = b"0123456789ABCDEF"
        tea_plain = b"ABCDEFGH"
        xxtea_plain = b"0123456789ABCDEF"

        tea_cipher = tea_encrypt(tea_plain, key)
        self.assertNotEqual(tea_cipher, tea_plain)
        self.assertEqual(tea_decrypt(tea_cipher, key), tea_plain)

        xtea_cipher = xtea_encrypt(tea_plain, key)
        self.assertNotEqual(xtea_cipher, tea_plain)
        self.assertEqual(xtea_decrypt(xtea_cipher, key), tea_plain)

        xxtea_cipher = xxtea_encrypt(xxtea_plain, key)
        self.assertNotEqual(xxtea_cipher, xxtea_plain)
        self.assertEqual(xxtea_decrypt(xxtea_cipher, key), xxtea_plain)

        rc5_cipher = rc5_encrypt(tea_plain, key)
        self.assertNotEqual(rc5_cipher, tea_plain)
        self.assertEqual(rc5_decrypt(rc5_cipher, key), tea_plain)

    def test_rc5_supports_tuple_and_custom_word_sizes(self):
        from regadgets.crypto import rc5_decrypt, rc5_encrypt

        key = b"secretkey"
        block = (0x12345678, 0x9ABCDEF0)
        cipher = rc5_encrypt(block, key)
        self.assertEqual(rc5_decrypt(cipher, key), block)

        small_block = (0x1234, 0xABCD)
        small_cipher = rc5_encrypt(small_block, key, rounds=8, word_size=16)
        self.assertEqual(rc5_decrypt(small_cipher, key, rounds=8, word_size=16), small_block)

    def test_aes_pcbc_roundtrip_is_consistent(self):
        from regadgets.crypto import AES128_pcbc_decrypt, AES128_pcbc_encrypt

        key = b"0123456789ABCDEF"
        iv = b"init-vector-1234"
        plaintext = b"pcbc extra compatibility"

        ciphertext = AES128_pcbc_encrypt(plaintext, key, iv)
        self.assertNotEqual(ciphertext, plaintext)
        self.assertEqual(AES128_pcbc_decrypt(ciphertext, key, iv), plaintext)


if __name__ == "__main__":
    unittest.main()
