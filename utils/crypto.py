import os
from cryptography.fernet import Fernet

def load_api_key():
    # Build absolute path relative to this file's location
    base_path = os.path.dirname(os.path.abspath(__file__))  # path to utils/
    key_path = os.path.join(base_path, "fernet.key")
    encrypted_path = os.path.join(base_path, "encrypted_key.bin")

    with open(key_path, "rb") as key_file:
        key = key_file.read()

    fernet = Fernet(key)

    with open(encrypted_path, "rb") as encrypted_file:
        encrypted_key = encrypted_file.read()

    decrypted_key = fernet.decrypt(encrypted_key).decode()
    return decrypted_key
