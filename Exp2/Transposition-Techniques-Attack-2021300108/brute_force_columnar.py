import math

def columnar_decrypt(cipher_text, keyword):
    key_order = [keyword.index(str(i + 1)) for i in range(len(keyword))]
    num_rows = math.ceil(len(cipher_text) / len(keyword))
    grid = [['X' for _ in range(len(keyword))] for _ in range(num_rows)]

    k = 0
    for i in key_order:
        for j in range(num_rows):
            if k < len(cipher_text):
                grid[j][i] = cipher_text[k]
                k += 1

    plain_text = []
    for i in range(num_rows):
        for j in range(len(keyword)):
            plain_text.append(grid[i][j])

    while plain_text[-1] == 'X':
        plain_text.pop()

    return ''.join(plain_text)

def brute_force_key(cipher_text, plain_text):
    keyword = "1234567"
    key_chars = list(keyword)
    return find_key(cipher_text, plain_text, key_chars, "")

def find_key(cipher_text, plain_text, key_chars, current_key):
    if len(current_key) == len(key_chars):
        decrypted_text = columnar_decrypt(cipher_text, current_key)
        if decrypted_text == plain_text:
            return current_key
        return None

    for i in range(len(key_chars)):
        if key_chars[i] not in current_key:
            found_key = find_key(cipher_text, plain_text, key_chars, current_key + key_chars[i])
            if found_key:
                return found_key
    return None

if __name__ == "__main__":
    text1 = "attackpostponeduntiltwoam"
    encrypted1 = "ttnaaptmtsuoaodwcoiXknlXpetX"
    text2 = "meetmeatthepark"
    encrypted2 = "mtketXehXteXmpXeaXarX"
    text3 = "defendtheeastwall"
    encrypted3 = "twXdtXnsXeaXfeleeldha"

    print(brute_force_key(encrypted1, text1))
    print(brute_force_key(encrypted2, text2))
    print(brute_force_key(encrypted3, text3))