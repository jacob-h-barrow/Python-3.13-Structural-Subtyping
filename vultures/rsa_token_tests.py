from rsa_crypto import RSA_Crypto, create_rsa_key_object
from Crypto.PublicKey import RSA

from rsa_token import RSA_Token_Encryption, RSA_Token_Decryption

import unittest
import json

class Test_RSA_Token(unittest.TestCase):
    def setUp(self):
        self.rsa_obj_1 = RSA_Crypto()
        self.rsa_obj_2 = RSA_Crypto()
        
        self.key_pair_1 = self.rsa_obj_1.export_keys()
        self.key_pair_2 = self.rsa_obj_1.export_keys()
        
        self.rsa_token_1 = RSA_Token_Encryption(self.key_pair_1, self.key_pair_2["public_key"], "Marlins#12345", 111, 86400)
        
    def test_decrypt_token(self):
        encrypted_token = self.rsa_token_1.encrypt_token()
        
        rsa_token_2 = RSA_Token_Decryption(self.key_pair_2, self.key_pair_1["public_key"], encrypted_token)
        
        result = rsa_token_2.all_in_one()
        
        self.assertEqual(isinstance(result, dict), True, "Decrypting the token didn't work!")
