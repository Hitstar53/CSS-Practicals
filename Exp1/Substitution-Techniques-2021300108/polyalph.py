def vigenere_encrypt(plaintext, key):
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    plaintext_int = [ord(i) for i in plaintext.upper()]
    ciphertext = ""
    for i in range(len(plaintext_int)):
        if 65 <= plaintext_int[i] <= 90:  # Ensure it's an uppercase letter
            value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
            ciphertext += chr(value + 65)
        else:
            ciphertext += chr(
                plaintext_int[i]
            )  # Non-alphabetical characters are unchanged
    return ciphertext


def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext.upper()]
    plaintext = ""
    for i in range(len(ciphertext_int)):
        if 65 <= ciphertext_int[i] <= 90:  # Ensure it's an uppercase letter
            value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
            plaintext += chr(value + 65)
        else:
            plaintext += chr(
                ciphertext_int[i]
            )  # Non-alphabetical characters are unchanged
    return plaintext


if __name__ == "__main__":
    key = input("Enter key: ")
    plaintext = input("Enter text: ")
    ciphertext = vigenere_encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext}")
    decrypted_text = vigenere_decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted_text}")