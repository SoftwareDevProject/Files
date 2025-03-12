# Importing modules
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# password 
data = b'password'

# Creation of encryption key
key = get_random_bytes(16)

# Encryption
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce

print(ciphertext)

# Decryption
decryptionCipher = AES.new(key,AES.MODE_EAX, nonce)
ddata = decryptionCipher.decrypt_and_verify(ciphertext, tag)

print(ddata)

class Entry:
  def __init__(email, password, key, nonce):
    self.email = email
    self.password = password
    self.key = key
    self.nonce = nonce
    
