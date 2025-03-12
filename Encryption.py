# Importing modules
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Entry class that defines what an entry will consist of when its stored
class Entry:
    def __init__(self, email, password, key, nonce, tag):
        self.email = email
        self.password = password
        self.key = key
        self.nonce = nonce
        self.tag = tag

    # Print function in entry class just to see what things look like
    def print(self):
        print("Email: " + self.email + " Password: ")
        print(self.password)
        print(self.key)
        print(self.nonce)
        print(self.tag)

# Encrypt function
def encrypt(email, password):
    # Creation of encryption key
    key = get_random_bytes(16)

    # Encryption
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())
    nonce = cipher.nonce

    new_entry = Entry(email, ciphertext, key, nonce, tag)

    # Need to look into this, password key nonce and tag will not be able to be written to file due to decoding errors
    #file = open("entries.txt", "w")
    #file.write(new_entry.email + "," + new_entry.password + "," + new_entry.key + "," + new_entry.nonce + tag)
    #file.close()

    new_entry.print()
    return new_entry

# Decrypt function
def decrypt(ciphertext, key, nonce, tag):
    decryptionCipher = AES.new(key, AES.MODE_EAX, nonce)
    ddata = decryptionCipher.decrypt_and_verify(ciphertext, tag)
    return ddata

# Test case
def test():
    new_entry1 = Entry("j", "j", "", "", "")
    encrypted_entry = encrypt(new_entry1.email, new_entry1.password)
    print(decrypt(encrypted_entry.password, encrypted_entry.key, encrypted_entry.nonce, encrypted_entry.tag))

test()
