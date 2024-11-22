import itertools

def decrypt(ciphertext, key):
    plaintext = []
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    key = key.upper()

    for i in range(len(ciphertext)):
        c = ciphertext[i]
        k = key[i % len(key)]
        decrypted_char = chr((ord(c) - ord(k) + 26) % 26 + ord('A'))
        plaintext.append(decrypted_char)

    return ''.join(plaintext)

def brute_force_poly_alphabetic_cipher(ciphertext, expected_plaintext, max_key_length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for length in range(1, max_key_length + 1):
        for key_tuple in itertools.product(alphabet, repeat=length):
            key = ''.join(key_tuple)
            decrypted_text = decrypt(ciphertext, key)
            if decrypted_text == expected_plaintext:
                return key
    return None

if __name__ == "__main__":
    cipher_text = "IOWR"
    excepted_plaintext = "TEST"
    key = brute_force_poly_alphabetic_cipher(cipher_text, excepted_plaintext, 5)
    print(f"Key: {key}")
    print(f"Decrypted text: {decrypt(cipher_text, key)}")