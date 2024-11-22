def generate_playfair_key(keyword):
    keyword = "".join(dict.fromkeys(keyword.upper().replace("J", "I")))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_matrix = [[None for _ in range(5)] for _ in range(5)]
    used = set()
    
    i, j = 0, 0
    for char in keyword:
        if char not in used and char in alphabet:
            key_matrix[i][j] = char
            used.add(char)
            j += 1
            if j == 5:
                i += 1
                j = 0

    for char in alphabet:
        if char not in used:
            key_matrix[i][j] = char
            used.add(char)
            j += 1
            if j == 5:
                i += 1
                j = 0
                
    return key_matrix

def prepare_text(plaintext):
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    prepared_text = ""
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i + 1] if i + 1 < len(plaintext) else "X"
        if a == b:
            prepared_text += a + "X"
            i += 1
        else:
            prepared_text += a + b
            i += 2
    if len(prepared_text) % 2 != 0:
        prepared_text += "X"
    return prepared_text

def playfair_encrypt(plaintext, key_matrix):
    def get_position(char):
        for i, row in enumerate(key_matrix):
            if char in row:
                return i, row.index(char)
        return None

    plaintext = prepare_text(plaintext)
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        row1, col1 = get_position(a)
        row2, col2 = get_position(b)
        if row1 == row2:
            # Same row: shift right
            ciphertext += key_matrix[row1][(col1 + 1) % 5]
            ciphertext += key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            # Same column: shift down
            ciphertext += key_matrix[(row1 + 1) % 5][col1]
            ciphertext += key_matrix[(row2 + 1) % 5][col2]
        else:
            # Rectangle: swap r and c
            ciphertext += key_matrix[row1][col2]
            ciphertext += key_matrix[row2][col1]

    return ciphertext

def playfair_decrypt(ciphertext, key_matrix):
    def get_position(char):
        for i, row in enumerate(key_matrix):
            if char in row:
                return i, row.index(char)
        return None

    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row1, col1 = get_position(a)
        row2, col2 = get_position(b)
        if row1 == row2:
            # Same row: shift left
            plaintext += key_matrix[row1][(col1 - 1) % 5]
            plaintext += key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            # Same column: shift up
            plaintext += key_matrix[(row1 - 1) % 5][col1]
            plaintext += key_matrix[(row2 - 1) % 5][col2]
        else:
            # Rectangle: swap r and c
            plaintext += key_matrix[row1][col2]
            plaintext += key_matrix[row2][col1]

    return plaintext

if __name__ == "__main__":
    key_matrix = generate_playfair_key(input("Enter keyword: "))
    plaintext = input("Enter text: ")
    ciphertext = playfair_encrypt(plaintext, key_matrix)
    print(f"Ciphertext: {ciphertext}")
    decrypted_text = playfair_decrypt(ciphertext, key_matrix)
    print(f"Decrypted text: {decrypted_text}")
