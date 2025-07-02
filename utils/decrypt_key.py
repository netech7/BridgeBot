# decrypt_key.py
import os
from dotenv import load_dotenv

def get_decrypted_api_key():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


# from cryptography.fernet import Fernet

# def get_decrypted_api_key():
#     with open("fernet.key", "rb") as kf:
#         key = kf.read()
#     with open("encrypted_key.bin", "rb") as ef:
#         encrypted_key = ef.read()
#     return Fernet(key).decrypt(encrypted_key).decode()
