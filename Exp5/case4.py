from sha512 import sha512
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


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


def send(message: str , seed: str):
    message_seed = message + seed
    hash_message = sha512(message_seed)
    message_send = message + hash_message
    encrypted = aes_encrypt(aes_key , message_send)
    print("Message:" , message)
    print("Sending encrypted message:", encrypted)
    print("Hash :", hash_message)
    return encrypted

def receive(encrypted_message : str , seed: str):
    message_decrypted = aes_decrypt(encrypted_message , aes_key)
    hash_message = message_decrypted[-128:]
    message = message_decrypted[:-128]
    expected_hash_message = sha512(message + seed)
    try:
        assert expected_hash_message == hash_message
        print(f"Message hashes matching\nMessage : {message}\nHash : {hash_message}")
        return message
    except AssertionError:
        print("Message hashes not matching! Message corrupted")
        return None

aes_key = hashlib.sha256(b'secret_key').digest()
seed_test = "secretmessage"
sent1 = send("Hatim" , seed_test)
recvd1 = receive(sent1 , seed_test)


