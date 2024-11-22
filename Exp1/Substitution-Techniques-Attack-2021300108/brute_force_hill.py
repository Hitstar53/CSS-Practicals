MOD = 26
def decrypt_hill_cipher(ciphertext, key_matrix):
    plaintext = []
    ciphertext = ciphertext.upper().replace(" ", "")

    for i in range(0, len(ciphertext), 2):
        vector = [
            ord(ciphertext[i]) - ord('A'),
            ord(ciphertext[i + 1]) - ord('A')
        ]

        decrypted_vector = multiply_matrix_and_vector(inverse_matrix(key_matrix), vector)

        for j in range(2):
            decrypted_vector[j] = (decrypted_vector[j] + MOD) % MOD
            plaintext.append(chr(decrypted_vector[j] + ord('A')))

    return ''.join(plaintext)

def inverse_matrix(matrix):
    dete = mod_inverse(determinant(matrix), MOD)

    adjugate = [
        [matrix[1][1], -matrix[0][1]],
        [-matrix[1][0], matrix[0][0]]
    ]

    for i in range(2):
        for j in range(2):
            adjugate[i][j] = (adjugate[i][j] * dete + MOD) % MOD

    return adjugate

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 1

def determinant(matrix):
    return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % MOD

def multiply_matrix_and_vector(matrix, vector):
    result = [0, 0]
    result[0] = matrix[0][0] * vector[0] + matrix[0][1] * vector[1]
    result[1] = matrix[1][0] * vector[0] + matrix[1][1] * vector[1]
    return result

def brute_force_hill_cipher(ciphertext, expected_plaintext):
    for a in range(26):
        for b in range(26):
            for c in range(26):
                for d in range(26):
                    key_matrix = [[a, b], [c, d]]
                    if is_invertible(key_matrix):
                        decrypted_text = decrypt_hill_cipher(ciphertext, key_matrix)
                        if decrypted_text.startswith(expected_plaintext):
                            return key_matrix
    return None

def is_invertible(matrix):
    det = determinant(matrix)
    return det != 0 and gcd(det, 26) == 1

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

if __name__ == "__main__":
    cypher_text = "BDFS"
    expected_plaintext = "TEST"
    
    key = brute_force_hill_cipher(cypher_text, expected_plaintext)
    print(f"Key: {key}")
    print(f"Decrypted text: {decrypt_hill_cipher(cypher_text, key)}")