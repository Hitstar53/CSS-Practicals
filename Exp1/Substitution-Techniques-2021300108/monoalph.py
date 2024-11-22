import random
import string

def generate_cipher_alphabet():
    alphabet = list(string.ascii_lowercase)
    cipher_alphabet = alphabet.copy()
    random.shuffle(cipher_alphabet)
    return "".join(cipher_alphabet)

def create_cipher_dict(cipher_alphabet, mode="encrypt"):
    plain_alphabet = string.ascii_lowercase
    if mode == "encrypt":
        return dict(zip(plain_alphabet, cipher_alphabet))
    else:
        return dict(zip(cipher_alphabet, plain_alphabet))

def monoalphabetic_cipher(text, cipher_alphabet, mode="encrypt"):
    cipher_dict = create_cipher_dict(cipher_alphabet, mode)
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char_lower = char.lower()
            if char_lower in cipher_dict:
                encrypted_char = cipher_dict[char_lower]
                result += encrypted_char.upper() if is_upper else encrypted_char
            else:
                result += char
        else:
            result += char
    return result


if __name__ == "__main__":
    text = input("Enter text: ")
    cipher_alphabet = generate_cipher_alphabet()
    encrypted = monoalphabetic_cipher(text, cipher_alphabet)
    decrypted = monoalphabetic_cipher(encrypted, cipher_alphabet, mode="decrypt")
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
