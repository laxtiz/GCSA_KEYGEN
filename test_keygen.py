import unittest
import keygen


class TestKeygen(unittest.TestCase):
    def test_decrypt(self):
        plain_text = "-123456789"
        cipher_text = "QBxOPKM8eFHhI4wO/tf2lQ=="
        self.assertEqual(plain_text, keygen.decrypt(cipher_text))

    def test_encrypt(self):
        plain_text = "-123456789"
        cipher_text = "QBxOPKM8eFHhI4wO/tf2lQ=="
        self.assertEqual(keygen.encrypt(plain_text), cipher_text)


if __name__ == "__main__":
    unittest.main()