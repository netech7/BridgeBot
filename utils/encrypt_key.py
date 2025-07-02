from cryptography.fernet import Fernet
import getpass

# Step 1: Create a Fernet encryption key
key = Fernet.generate_key()
fernet = Fernet(key)

# Step 2: Input your OpenAI API key
api_key = input("Enter your API key: ").strip()

# Step 3: Encrypt it
encrypted_key = fernet.encrypt(api_key.encode())

# Step 4: Save the encrypted key to a binary file
with open("encrypted_key.bin", "wb") as f:
    f.write(encrypted_key)

# Step 5: Save the Fernet key to a file (DO NOT COMMIT THIS!)
with open("fernet.key", "wb") as f:
    f.write(key)

print("\n✅ Your API key has been encrypted and saved.")
print("🔐 Store 'fernet.key' securely. Never share or push it to GitHub.")
