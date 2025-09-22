from .aes import AESCipher

import unittest
import json

class Test_AES_Crypto(unittest.TestCase):
    def setUp(self):
        self.aes_obj_1 = AESCipher("Marlins#12345678")
        self.aes_obj_2 = AESCipher("Marlins#12345678")
        
        self.message = "Hey there, unit cells are the best! #Chemistry"
        self.encrypted_message_1 = self.aes_obj_1.encrypt(self.message)
        
        self.token = {"username": "jarvis", "result": {"accept": True}}
        self.encrypted_message_2 = self.aes_obj_1.encrypt(self.token)
        
    def test_decryption(self):
        decrypted_message = self.aes_obj_2.decrypt(self.encrypted_message_1)
        
        self.assertEqual(decrypted_message == self.message, True, "Decryption not working!")
        
    def test_token_decryption(self):
        decrypted_message = self.aes_obj_2.decrypt(self.encrypted_message_2)
        decrypted_message = json.loads(decrypted_message)
        
        self.assertEqual(decrypted_message == self.token, True, "Token decryption didn't work!")
        

