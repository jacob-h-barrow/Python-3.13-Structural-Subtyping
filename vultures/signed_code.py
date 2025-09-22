import pickle

from datetime import datetime

from rsa_crypto import RSA_Crypto, create_rsa_key_object
from rsa_utils
# Need to create code_signing db that interfaces with dbUtils.py
from signed_code_utils import db

class Code:
    def __init__(self, key_pair: dict):
        self.rsa_cipher = RSA_Crypto(keys = [rsa_key_pair["public_key"], rsa_key_pair["private_key"]])
        
        self.filename = filename
        self.classname = classname
        
    def get_signed_code(self, others_public_key, filename: str, classname: str):
        # LEFT OFF BEFORE LUNCH HERE
        pass
