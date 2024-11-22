def caesar_decrypt(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            plaintext += chr((ord(char) - shift_amount - shift) % 26 + shift_amount)
        else:
            plaintext += char
    return plaintext


def caesar_bruteforce(ciphertext, text):
    for shift in range(1, 26):
        decrypted_text = caesar_decrypt(ciphertext, shift)
        
        if text.lower() in decrypted_text.lower():
            print(f"Shift: {shift}, text: {decrypted_text}")

if __name__ == "__main__":
    text = input("Enter text: ")
    ciphertext = input("Enter ciphertext: ")
    caesar_bruteforce(ciphertext, text)