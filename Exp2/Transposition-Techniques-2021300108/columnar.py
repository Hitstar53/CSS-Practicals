import math

def columnar_encrypt(text, keyword):
    key_order = [keyword.index(str(i + 1)) for i in range(len(keyword))]

    num_rows = math.ceil(len(text) / len(keyword))
    grid = [['X' for _ in range(len(keyword))] for _ in range(num_rows)]

    k = 0
    for i in range(num_rows):
        for j in range(len(keyword)):
            if k < len(text):
                grid[i][j] = text[k]
                k += 1

    cipher_text = []
    for i in key_order:
        for j in range(num_rows):
            cipher_text.append(grid[j][i])

    return ''.join(cipher_text)

if __name__ == "__main__":
    text1 = "attackpostponeduntiltwoam"
    keyword1 = "4312567"
    text2 = "meetmeatthepark"
    keyword2 = "1234567"
    text3 = "defendtheeastwall"
    keyword3 = "7654321"

    print(columnar_encrypt(text1, keyword1))
    print(columnar_encrypt(text2, keyword2))
    print(columnar_encrypt(text3, keyword3))