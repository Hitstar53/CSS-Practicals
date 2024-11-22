def rail_fence_encrypt(plaintext, key):
    rails = [""]*key
    rail = 0
    direction = 1  # 1 for down, -1 for up

    for char in plaintext:
        rails[rail] += char
        rail += direction
        if rail == 0 or rail == key - 1:
            direction *= -1

    return "".join(rails)


def rail_fence_decrypt(ciphertext, key):
    rails = [""]*key
    index = 0
    pattern = [0] * len(ciphertext)

    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        pattern[i] = rail
        rail += direction
        if rail == 0 or rail == key - 1:
            direction *= -1

    for rail_num in range(key):
        for i in range(len(ciphertext)):
            if pattern[i] == rail_num:
                rails[rail_num] += ciphertext[index]
                index += 1

    result = ""
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        result += rails[rail][0]
        rails[rail] = rails[rail][1:]
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    return result


if __name__ == "__main__":
    plaintext = "HELLOWORLD"
    num_rails = 3

    ciphertext = rail_fence_encrypt(plaintext, num_rails)
    print(f"Ciphertext: {ciphertext}")

    decrypted = rail_fence_decrypt(ciphertext, num_rails)
    print(f"Decrypted: {decrypted}")