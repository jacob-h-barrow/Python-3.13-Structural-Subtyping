from .rsa_crypto import RSA_Crypto, create_rsa_key_object
from Crypto.PublicKey import RSA

import unittest
import json

class Test_RSA_Crypto(unittest.TestCase):
    def setUp(self):
        self.rsa_obj_1 = RSA_Crypto()
        self.rsa_obj_2 = RSA_Crypto()
        
        self.key_pair_1 = self.rsa_obj_1.export_keys()
        
    def test_decryption_text(self):
        message = "attack at dawn"
        
        cipher_text = self.rsa_obj_1.encrypt(message, self.rsa_obj_2.pubKey_obj)
        decrypted_message = self.rsa_obj_2.decrypt(cipher_text)
        
        self.assertEqual(message == decrypted_message, True, "Encryption did not work properly!")
        
    def test_decryption_token(self):
        data = {"username": "jarvis", "result": {"accept": True}}
        
        cipher_text = self.rsa_obj_2.encrypt(data, self.rsa_obj_1.pubKey_obj)
        decrypted_message = json.loads(self.rsa_obj_1.decrypt(cipher_text))
        
        self.assertEqual(data == decrypted_message, True, "Token encryption did not work properly!")
        
    def test_export_public_key(self):
        data = self.key_pair_1["public_key"]

        values = len(data.keys())
        
        self.assertEqual(isinstance(data, dict), True, "Public key export data type didn't match!")
        self.assertEqual(values, 2, "Public key export data wasn't the right length!")
        
    def test_export_private_key(self):
        data = self.key_pair_1["private_key"]
        
        values = len(data.keys())
        
        self.assertEqual(isinstance(data, dict), True, "Private key export data type didn't match!")
        self.assertEqual(values, 6, "Private key export data wasn't the right length!")
        
    def test_create_rsa_object_from_memory(self):
        pub = create_rsa_key_object(self.key_pair_1["public_key"])
        priv = create_rsa_key_object(self.key_pair_1["private_key"], public = False)
        
        pub_correct = isinstance(pub, RSA.RsaKey)
        priv_correct = isinstance(priv, RSA.RsaKey)
        
        self.assertEqual(pub_correct and priv_correct, True, "In-memory RSA object creation failed!")
        
    def test_signature_token(self):
        data = {"username": "jarvis", "result": {"accept": True}}
        
        signature = self.rsa_obj_2.sign_message(data)
        legitimate = self.rsa_obj_1.verify_signature(data, signature, self.rsa_obj_2.pubKey_obj)
        
        self.assertEqual(legitimate, True, "Signature didn't verify correctly!")
