from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from sha512 import sha512  


def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))  
    return cipher.iv + ciphertext  


def aes_decrypt(key, ciphertext):
    iv = ciphertext[:16] 
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size) 
    return plaintext.decode()

def hash_message(message):
    return sha512(message)

def encrypt_hash_of_message(message, key):
    message_hash = hash_message(message)  
    encrypted_hash = aes_encrypt(key, message_hash) 
    return encrypted_hash

def concatenate_message_and_encrypted_hash(message, encrypted_hash):
    return message.encode() + encrypted_hash

def extract_message_and_encrypted_hash(concatenated_data):
    message = concatenated_data[:-160].decode()
    encrypted_hash = concatenated_data[-160:]
    return message, encrypted_hash


def decrypt_and_verify(concatenated_data, key):
    message, encrypted_hash = extract_message_and_encrypted_hash(concatenated_data)
    
    decrypted_hash = aes_decrypt(key, encrypted_hash)  
    
    message_hash = hash_message(message)  

    if decrypted_hash == message_hash:
        return True
    else:
        return False

if __name__ == "__main__":
    message = "Hello,world!"
    
    aes_key = hashlib.sha256(b'secret_key').digest()
    
    encrypted_hash = encrypt_hash_of_message(message, aes_key)
    
    concatenated_data = concatenate_message_and_encrypted_hash(message, encrypted_hash)
    
    verification_status = decrypt_and_verify(concatenated_data, aes_key)
    
    if verification_status:
        print("Message integrity verified!")
    else:
        print("Message integrity verification failed!")
