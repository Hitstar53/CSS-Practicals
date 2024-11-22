def generate_playfair_square(key):
    key = key.upper().replace("J", "I")
    key_builder = []
    seen = set()

    for c in key:
        if c not in seen and 'A' <= c <= 'Z':
            key_builder.append(c)
            seen.add(c)

    for c in range(ord('A'), ord('Z') + 1):
        if chr(c) != 'J' and chr(c) not in seen:
            key_builder.append(chr(c))
            seen.add(chr(c))

    key_square = [key_builder[i:i + 5] for i in range(0, 25, 5)]
    return key_square

def decrypt_playfair(ciphertext, key_square):
    plaintext = []
    digraphs = create_digraphs(ciphertext.upper().replace("J", "I"))

    for digraph in digraphs:
        pos1 = find_position(key_square, digraph[0])
        pos2 = find_position(key_square, digraph[1])

        if pos1[0] == pos2[0]:  # Same row
            plaintext.append(key_square[pos1[0]][(pos1[1] + 4) % 5])
            plaintext.append(key_square[pos2[0]][(pos2[1] + 4) % 5])
        elif pos1[1] == pos2[1]:  # Same column
            plaintext.append(key_square[(pos1[0] + 4) % 5][pos1[1]])
            plaintext.append(key_square[(pos2[0] + 4) % 5][pos2[1]])
        else:  # Rectangle
            plaintext.append(key_square[pos1[0]][pos2[1]])
            plaintext.append(key_square[pos2[0]][pos1[1]])

    return ''.join(plaintext)

def create_digraphs(text):
    digraphs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            digraphs.append(text[i] + text[i + 1])
        else:
            digraphs.append(text[i] + 'X')
        i += 2
    return digraphs

def find_position(key_square, c):
    for i, row in enumerate(key_square):
        for j, char in enumerate(row):
            if char == c:
                return (i, j)
    return None

def brute_force_playfair(ciphertext, expected_plaintext):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    characters = list(alphabet)
    return permute_and_decrypt(characters, "", 3, ciphertext, expected_plaintext)

def permute_and_decrypt(characters, prefix, n, ciphertext, expected_plaintext):
    if len(prefix) == n:
        key_square = generate_playfair_square(prefix)
        plaintext_candidate = decrypt_playfair(ciphertext, key_square)
        if plaintext_candidate == expected_plaintext:
            return prefix
        return None

    for i in range(len(characters)):
        c = characters.pop(i)
        found_key = permute_and_decrypt(characters, prefix + c, n, ciphertext, expected_plaintext)
        characters.insert(i, c)
        if found_key:
            return found_key

    return None

if __name__ == "__main__":
    cyphertext = "SATU"
    expected_plaintext = "TEST"
    
    key = brute_force_playfair(cyphertext, expected_plaintext)
    print(f"Key: {key}")
    print(f"Plaintext: {decrypt_playfair(cyphertext, generate_playfair_square(key))}")