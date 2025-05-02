# Encryption.py
# Written by: Kenneth Hook, Jacob Lee, Samuel Ofori-Addi, Meera Pillai
# Purpose: This code is the handles the encryption and decryption for the application.

# Imports
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import json

# File paths
MASTER_FILE = "master.dat"
ENTRIES_FILE = "entries.txt"
SECURITY_FILE = "security.dat"

# Predefined security questions
SECURITY_QUESTIONS = [
    "What is your pet's name?",
    "What is the name of your high school?",
    "What is your mother's middle name?",
    "What is your father's middle name?",
    "What is your favorite color?"
]

# Retrieves all security questions
def get_all_security_questions():
    return SECURITY_QUESTIONS

# Security question handling
def set_security_question(question, answer):
    data = {
        "question": question,
        "answer_hash": hashlib.sha256(answer.lower().strip().encode()).hexdigest()
    }
    with open(SECURITY_FILE, 'w') as f:
        json.dump(data, f)

# Retrieves security question that user answered to set master password
def get_security_question():
    if not os.path.exists(SECURITY_FILE):
        return None
    with open(SECURITY_FILE, 'r') as f:
        data = json.load(f)
    return data.get("question")

# Verifies answer to security question is correct to allow for password reset
def verify_security_answer(answer):
    if not os.path.exists(SECURITY_FILE):
        return False
    with open(SECURITY_FILE, 'r') as f:
        data = json.load(f)
    answer_hash = hashlib.sha256(answer.lower().strip().encode()).hexdigest()
    return data.get("answer_hash") == answer_hash

# Hash a password (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Save hashed master password
def set_master_password(password):
    with open(MASTER_FILE, "w") as f:
        f.write(hash_password(password))


# Check if config exists
def master_password_exists():
    return os.path.exists(MASTER_FILE)


# Verify entered password
def verify_master_password(input_password):
    if not master_password_exists():
        return False

    with open(MASTER_FILE, "r") as f:
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

    with open(ENTRIES_FILE, "a") as f:
        f.write(f"{category},{email},{','.join(encoded_data)}\n")

# Decrypt password based on category and email equaling correct entry in txt file
def decrypt_password(category, email):
    with open(ENTRIES_FILE, "r") as f:
        for line in f:
            entry = line.strip().split(',')
            stored_category, stored_email = entry[0], entry[1]

            if stored_category == category and stored_email == email:
                encoded_data = entry[2:]  # Extract the encrypted data

                ciphertext = base64.b64decode(encoded_data[0])
                key = base64.b64decode(encoded_data[1])
                nonce = base64.b64decode(encoded_data[2])
                tag = base64.b64decode(encoded_data[3])

                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                decrypted_password = cipher.decrypt_and_verify(ciphertext, tag)

                return decrypted_password.decode('utf-8')

    # If no matching entry is found
    return None

# Load and return all entries
def load_entries():
    entries = []

    if not os.path.exists(ENTRIES_FILE):
        return entries

    with open(ENTRIES_FILE, "r") as f:

        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 6:
                continue
            category, email, *b64 = parts
            ciphertext, key, nonce, tag = [base64.b64decode(x) for x in b64]
            try:
                entries.append((category, email, ciphertext))

            except:
                pass  # decryption failed, skip

    return entries


# Overwrite all entries in the file
def overwrite_entries(entries):
    with open(ENTRIES_FILE, "w") as f:
        for category, email, password in entries:
            encrypt_and_store(category, email, password)
