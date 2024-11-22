def matrix_multiply(matrix1, matrix2, m):
    result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
            result[i][j] %= m
    return result

def matrix_mod_inverse(matrix, m):
    det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % m
    det_inv = pow(det, -1, m)
    return [
        [(matrix[1][1] * det_inv) % m, (-matrix[0][1] * det_inv) % m],
        [(-matrix[1][0] * det_inv) % m, (matrix[0][0] * det_inv) % m],
    ]

def hill_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += "X"

    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        pair = [[ord(plaintext[i]) - 65], [ord(plaintext[i + 1]) - 65]]
        result = matrix_multiply(key, pair, 26)
        ciphertext += chr(result[0][0] + 65) + chr(result[1][0] + 65)

    return ciphertext

def hill_decrypt(ciphertext, key):
    key_inverse = matrix_mod_inverse(key, 26)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        pair = [[ord(ciphertext[i]) - 65], [ord(ciphertext[i + 1]) - 65]]
        result = matrix_multiply(key_inverse, pair, 26)
        plaintext += chr(result[0][0] + 65) + chr(result[1][0] + 65)

    return plaintext

if __name__ == "__main__":
    key = [[7, 8], [11, 11]]
    plaintext = input("Enter text: ")
    ciphertext = hill_encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext}")
    decrypted_text = hill_decrypt(ciphertext, key)
    print(f"Decrypted text: {decrypted_text}")