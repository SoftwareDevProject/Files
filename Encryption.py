# Encryption.py

# Imports
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# Global Files
VAULT_FILE = "entries.txt"
CONFIG_FILE = "config.txt"

# Hash a password (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save hashed master password
def set_master_password(password):
    with open(CONFIG_FILE, "w") as f:
        f.write(hash_password(password))

# Check if config exists
def master_password_exists():
    return os.path.exists(CONFIG_FILE)

# Verify entered password
def verify_master_password(input_password):
    if not master_password_exists():
        return False
    with open(CONFIG_FILE, "r") as f:
        stored_hash = f.read().strip()
    return hash_password(input_password) == stored_hash

# Encrypt password entry and save to file
def encrypt_and_store(category, email, password):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())
    nonce = cipher.nonce

    encoded_data = [
        base64.b64encode(x).decode('utf-8')
        for x in [ciphertext, key, nonce, tag]
    ]

    with open(VAULT_FILE, "a") as f:
        f.write(f"{category},{email},{','.join(encoded_data)}\n")

# Load and decrypt all entries
def load_entries():
    entries = []
    if not os.path.exists(VAULT_FILE):
        return entries

    with open(VAULT_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 6:
                continue
            category, email, *b64 = parts
            ciphertext, key, nonce, tag = [base64.b64decode(x) for x in b64]
            try:
                cipher = AES.new(key, AES.MODE_EAX, nonce)
                password = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
                entries.append((category, email, password))
            except:
                pass  # decryption failed, skip
    return entries

# Overwrite all entries in the file
def overwrite_entries(entries):
    with open(VAULT_FILE, "w") as f:
        for category, email, password in entries:
            encrypt_and_store(category, email, password)
