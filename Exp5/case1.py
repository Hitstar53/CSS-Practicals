from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from sha512 import sha512  

def hash_message(message):
    return sha512(message) 


def aes_encrypt(key, data):
    if isinstance(data, str): 
        data = data.encode('utf-8')
    
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext 

def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16] 
    ciphertext = encrypted_data[16:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    original_message_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    original_message = original_message_bytes.decode('utf-8')
    return original_message

def encrypt_message_aes(message, key):
    message_hash = hash_message(message)
    
    combined_message = message + message_hash
    
    encrypted_data = aes_encrypt(key, combined_message)
    return encrypted_data

def decrypt_message_aes(encrypted_data, key):
    decrypted_message = aes_decrypt(encrypted_data, key)
    
    original_message = decrypted_message[:-128]  
    received_hash = decrypted_message[-128:]  
    
    computed_hash = hash_message(original_message)
    
    
    if received_hash == computed_hash:
        verification_status = True
    else:
        verification_status = False
    
    return original_message, verification_status


if __name__ == "__main__":
    
    aes_key = hashlib.sha256(b'secret_key').digest()
   
    message = "Hello this is Hatim"
 
    encrypted_data = encrypt_message_aes(message, aes_key)
    print("Encrypted data:", encrypted_data)

    decrypted_message, verification_status = decrypt_message_aes(encrypted_data,aes_key)


    print("Decrypted message:", decrypted_message)
    print("Verification status:", verification_status)
