import os
import ast
import re
import hashlib
import base64
from Crypto.Cipher import AES

Author = "Denventa"
class CodeDeobfuscator:
    def __init__(self):
        self.text = """"""

    def clear_console(self):
        # Detect operating system and clear console
        os.system("cls" if os.name == "nt" else "clear")

    def derive_key_and_iv(self, password, salt):
        derived_key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        key = derived_key[:16]
        iv = derived_key[16:]
        return key, iv

    def aes_decrypt(self, encrypted_data, key):
        decoded_data = base64.b85decode(encrypted_data)
        salt = decoded_data[:8]
        key, iv = self.derive_key_and_iv(key, salt)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        decrypted_data = cipher.decrypt(decoded_data[8:])
        return decrypted_data.decode()

    def deobfuscate_code(self, input_file, output_file):
        with open(input_file, "r") as file:
            lines = file.readlines()

            for i, line in enumerate(lines, start=1):
                match = re.search(r"obfuscate = (.+)", line)
                if match:
                    obfuscated_code_str = match.group(1)
                    line_number = i
                    break

            if ".replace('\\n','')]))" not in obfuscated_code_str:
                while ".replace('\\n','')]))" not in obfuscated_code_str:
                    obfuscated_code_str += lines[line_number]
                    line_number += 1

            obfuscated_code = str(eval(obfuscated_code_str))

            code_dictionary = ast.literal_eval(obfuscated_code)

            encrypted_data = list(code_dictionary.values())[0]
            encryption_key = list(code_dictionary.keys())[0][1:-1]

        with open(output_file, "w", encoding="utf-8") as output:
            decrypted_code = self.aes_decrypt(encrypted_data, encryption_key)
            output.write(decrypted_code)
            print(f"File {input_file} successfully deobfuscated and saved in {output_file}!\n")


if __name__ == "__main__":
    deobfuscator = CodeDeobfuscator()
    deobfuscator.clear_console()
    input_filename = input("Masukkan nama file -> ")
    output_filename = input("Enter the name of the output file -> ")
    deobfuscator.deobfuscate_code(input_filename, output_filename)
