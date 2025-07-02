# key_setup.py

from cryptography.fernet import Fernet

# STEP 1: Generate encryption key
key = Fernet.generate_key()
with open("fernet.key", "wb") as fk:
    fk.write(key)

# STEP 2: Encrypt the API key
api_key = input("Enter your Gemini API key: ").encode()
encrypted = Fernet(key).encrypt(api_key)
with open("encrypted_key.bin", "wb") as ef:
    ef.write(encrypted)

print("✅ Encrypted key and fernet.key generated successfully.")
