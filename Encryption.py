# Encryption.py
# Written by: Kenneth Hook, Jacob Lee, Samuel Ofori-Addi, Meera Pillai
# Purpose: This code is the handles the encryption and decryption for the application.

# Imports

import hashlib
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

def get_all_security_questions():
    return SECURITY_QUESTIONS

# Generate a key based on the master password
def _generate_key(password):
    return hashlib.sha256(password.encode()).digest()

# Master password handling
def set_master_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(MASTER_FILE, 'w') as f:
        f.write(hashed)

def verify_master_password(password):
    if not os.path.exists(MASTER_FILE):
        return False
    with open(MASTER_FILE, 'r') as f:
        stored = f.read()
    return hashlib.sha256(password.encode()).hexdigest() == stored

def master_password_exists():
    return os.path.exists(MASTER_FILE)

# Security question handling
def set_security_question(question, answer):
    data = {
        "question": question,
        "answer_hash": hashlib.sha256(answer.lower().strip().encode()).hexdigest()
    }
    with open(SECURITY_FILE, 'w') as f:
        json.dump(data, f)

def get_security_question():
    if not os.path.exists(SECURITY_FILE):
        return None
    with open(SECURITY_FILE, 'r') as f:
        data = json.load(f)
    return data.get("question")

def verify_security_answer(answer):
    if not os.path.exists(SECURITY_FILE):
        return False
    with open(SECURITY_FILE, 'r') as f:
        data = json.load(f)
    answer_hash = hashlib.sha256(answer.lower().strip().encode()).hexdigest()
    return data.get("answer_hash") == answer_hash

# Entry encryption (simple write and read)
def encrypt_and_store(category, email, password):
    with open(ENTRIES_FILE, 'a') as f:
        f.write(f"{category},{email},{password}\n")

def load_entries():
    if not os.path.exists(ENTRIES_FILE):
        return []
    with open(ENTRIES_FILE, 'r') as f:
        lines = f.readlines()
    return [tuple(line.strip().split(',')) for line in lines]

def overwrite_entries(entries):
    with open(ENTRIES_FILE, 'w') as f:
        for cat, email, pw in entries:
            f.write(f"{cat},{email},{pw}\n")
