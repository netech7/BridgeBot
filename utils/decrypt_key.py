# decrypt_key.py
from cryptography.fernet import Fernet

def get_decrypted_api_key():
    with open("fernet.key", "rb") as kf:
        key = kf.read()
    with open("encrypted_key.bin", "rb") as ef:
        encrypted_key = ef.read()
    return Fernet(key).decrypt(encrypted_key).decode()
#print(get_decrypted_api_key())

# def get_decrypted_api_key():
#     with open("fernet.key", "rb") as f:
#         key = f.read()
#     with open("encrypted_key.bin", "rb") as f:
#         encrypted_api_key = f.read()

#     fernet = Fernet(key)
#     decrypted_key = fernet.decrypt(encrypted_api_key).decode()
#     return decrypted_key
