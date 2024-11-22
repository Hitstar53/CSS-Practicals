def caesar_cipher(text, shift, mode="encrypt"):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            if mode == "encrypt":
                shifted = (ord(char) - ascii_offset + shift) % 26
            else:  # decrypt
                shifted = (ord(char) - ascii_offset - shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result

if __name__ == "__main__":
    text = input("Enter text: ")
    shift = int(input("Enter shift: "))
    encrypted = caesar_cipher(text, shift)
    decrypted = caesar_cipher(encrypted, shift, mode="decrypt")
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")